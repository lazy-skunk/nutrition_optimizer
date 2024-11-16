from pulp import LpMaximize, LpMinimize, LpProblem, LpStatus, LpVariable

from src.constraint import Constraint
from src.food_information import FoodInformation
from src.objective import Objective


class NutritionOptimizer:
    _GRAM_CALCULATION_FACTOR = 100

    def __init__(
        self,
        foods: list[FoodInformation],
        objective: Objective,
        constraints: list[Constraint],
    ) -> None:
        self.foods: list[FoodInformation] = foods
        self.objective: Objective = objective
        self.constraints: list[Constraint] = constraints

        self.lp_variables: dict[str, LpVariable] = {}
        self.problem: LpProblem = LpProblem(
            "制約に基づきカロリーを最大化", sense=LpMaximize
        )

        # この辺は配列か辞書にまとめて簡単にしたいかも。
        self.total_energy: int = 0
        self.total_protein: int = 0
        self.total_fat: int = 0
        self.total_carbohydrates: int = 0

        self._setup_variables()
        self._define_problem()
        self._calculate_total_nutrients()

    def _setup_variables(self) -> None:
        for food_item in self.foods:
            self.lp_variables[food_item.name] = LpVariable(
                food_item.name,
                lowBound=food_item.minimum_intake,
                upBound=food_item.maximum_intake,
                cat="Integer",
            )

    def _define_problem(self) -> None:
        if self.objective.problem == "minimize":
            self.problem = LpProblem(
                f"minimize_{self.objective.nutritional_component}",
                LpMinimize,
            )
        else:
            self.problem = LpProblem(
                f"maximize_{self.objective.nutritional_component}",
                LpMaximize,
            )

    def _calculate_total_nutrients(self) -> None:
        # TODO: 1個当たりのグラム数は画面から入力できるようにしたい。
        GRAMS_PER_UNIT = 1
        for food_item in self.foods:
            self.total_energy += (
                food_item.energy
                * (GRAMS_PER_UNIT * self.lp_variables[food_item.name])
                / self._GRAM_CALCULATION_FACTOR
            )
            self.total_protein += (
                food_item.protein
                * (GRAMS_PER_UNIT * self.lp_variables[food_item.name])
                / self._GRAM_CALCULATION_FACTOR
            )
            self.total_fat += (
                food_item.fat
                * (GRAMS_PER_UNIT * self.lp_variables[food_item.name])
                / self._GRAM_CALCULATION_FACTOR
            )
            self.total_carbohydrates += (
                food_item.carbohydrates
                * (GRAMS_PER_UNIT * self.lp_variables[food_item.name])
                / self._GRAM_CALCULATION_FACTOR
            )

    def add_constraints(self) -> None:
        self._calculate_total_nutrients()

        self.problem += self.total_energy, "カロリーの最大化"
        self.problem += self.total_energy <= 1700, "カロリーの上限"
        # self.problem += self.total_protein <= 160, "たんぱく質のグラム数上限"
        # self.problem += self.total_protein >= 150, "たんぱく質のグラム数下限"

        # MAX_FAT_RATIO = 0.3  # 20%
        # self.problem += (
        #     self.total_fat * 9 <= self.total_kcal * MAX_FAT_RATIO,
        #     "脂質の割合制限",
        # )

    def solve(self) -> None:
        self._setup_variables()
        self.add_constraints()
        self.problem.solve()

        if LpStatus[self.problem.status] == "Optimal":
            print("最適解が見つかりました。")
            for food in self.lp_variables.keys():
                print(f"{food}: {self.lp_variables[food].varValue}")

            print("###")
            print(f"総たんぱく質: {self.total_protein:.1f} g")
            print(f"総脂質: {self.total_fat:.1f} g")
            print(f"総炭水化物: {self.total_carbohydrates:.1f} g")
            print(f"総カロリー: {self.total_energy:.1f} kcal")

            total_energy = self.total_energy
            PROTEIN_KCAL_PER_GRAM = 4
            FAT_KCAL_PER_GRAM = 9
            CARBOHYDRATE_KCAL_PER_GRAM = 4

            protein_ratio = (
                (self.total_protein * PROTEIN_KCAL_PER_GRAM)
                / total_energy
                * 100
            )

            fat_ratio = (
                (self.total_fat * FAT_KCAL_PER_GRAM) / total_energy * 100
            )

            carbohydrate_ratio = (
                (self.total_carbohydrates * CARBOHYDRATE_KCAL_PER_GRAM)
                / total_energy
                * 100
            )

            print("### PFCバランス")
            print(f"たんぱく質割合: {protein_ratio:.1f}%")
            print(f"脂質割合: {fat_ratio:.1f}%")
            print(f"炭水化物割合: {carbohydrate_ratio:.1f}%")

        else:
            print("最適解が見つかりませんでした。")
