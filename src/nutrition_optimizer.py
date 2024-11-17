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

        # TODO: この辺は配列か辞書にまとめて簡単にしたいかも。
        self.total_energy: int = 0
        self.total_protein: int = 0
        self.total_fat: int = 0
        self.total_carbohydrates: int = 0

    def _initialize_lp_variables(self) -> None:
        for food_item in self.foods:
            self.lp_variables[food_item.name] = LpVariable(
                food_item.name,
                lowBound=food_item.minimum_intake,
                upBound=food_item.maximum_intake,
                cat="Integer",
            )

    def _initialize_lp_problem(self) -> None:
        problem = self.objective.problem
        nutrientional_component = self.objective.nutritional_component

        problem_type = LpMinimize if problem == "minimize" else LpMaximize

        self.problem = LpProblem(
            f"{problem}_{nutrientional_component}", problem_type
        )

        if nutrientional_component == "energy":
            target = self.total_energy
        elif nutrientional_component == "protein":
            target = self.total_protein
        elif nutrientional_component == "fat":
            target = self.total_fat
        elif nutrientional_component == "carbohydrates":
            target = self.total_carbohydrates
        else:
            raise ValueError(
                f"Unknown nutritional component: {nutrientional_component}"
            )

        self.problem += (target, f"{problem}_{nutrientional_component}")

    def _initialize_objective_variables(self) -> None:
        for food_item in self.foods:
            self.total_energy += (
                food_item.energy
                * (
                    food_item.grams_per_unit
                    * self.lp_variables[food_item.name]
                )
                / self._GRAM_CALCULATION_FACTOR
            )
            self.total_protein += (
                food_item.protein
                * (
                    food_item.grams_per_unit
                    * self.lp_variables[food_item.name]
                )
                / self._GRAM_CALCULATION_FACTOR
            )
            self.total_fat += (
                food_item.fat
                * (
                    food_item.grams_per_unit
                    * self.lp_variables[food_item.name]
                )
                / self._GRAM_CALCULATION_FACTOR
            )
            self.total_carbohydrates += (
                food_item.carbohydrates
                * (
                    food_item.grams_per_unit
                    * self.lp_variables[food_item.name]
                )
                / self._GRAM_CALCULATION_FACTOR
            )

    def _add_constraint_to_problem(self) -> None:
        # TODO: この辺がなんか長い。細分化したい。
        for constraint in self.constraints:
            nutritional_component = constraint.nutritional_component
            min_max = constraint.min_max
            value = constraint.value
            unit = constraint.unit

            if nutritional_component == "energy":
                nutrient_value = self.total_energy
            elif nutritional_component == "protein":
                nutrient_value = self.total_protein
            elif nutritional_component == "fat":
                nutrient_value = self.total_fat
            elif nutritional_component == "carbohydrates":
                nutrient_value = self.total_carbohydrates
            else:
                raise ValueError(
                    f"Unknown nutritional component: {nutritional_component}"
                )
            # TODO: 画面側の表現を普通の単位に変えたいかも。Amount(g) とかじゃなくて g だけの方が直感的かも。
            if unit == "amount" or unit == "energy":
                if min_max == "max":
                    self.problem += (
                        nutrient_value <= value,
                        # TODO: とりあえず固定値にしているけど、全体的に動的にしたいかも。
                        f"Max_{nutritional_component.capitalize()}_Amount",
                    )
                elif min_max == "min":
                    self.problem += (
                        nutrient_value >= value,
                        f"Min_{nutritional_component.capitalize()}_Amount",
                    )

            elif unit == "ratio":
                if nutritional_component == "fat":
                    total_fat_energy = (
                        self.total_fat * FoodInformation.FAT_ENERGY_PER_GRAM
                    )
                    if min_max == "max":
                        self.problem += (
                            total_fat_energy
                            <= self.total_energy
                            * (value / self._GRAM_CALCULATION_FACTOR),
                            f"Max_{nutritional_component.capitalize()}_Ratio",
                        )
                    elif min_max == "min":
                        self.problem += (
                            total_fat_energy
                            >= self.total_energy
                            * (value / self._GRAM_CALCULATION_FACTOR),
                            f"Min_{nutritional_component.capitalize()}_Ratio",
                        )
                else:
                    if min_max == "max":
                        self.problem += (
                            nutrient_value
                            <= self.total_energy
                            * (value / self._GRAM_CALCULATION_FACTOR),
                            f"Max_{nutritional_component.capitalize()}_Ratio",
                        )
                    elif min_max == "min":
                        self.problem += (
                            nutrient_value
                            >= self.total_energy
                            * (value / self._GRAM_CALCULATION_FACTOR),
                            f"Min_{nutritional_component.capitalize()}_Ratio",
                        )
            else:
                raise ValueError(f"Unknown unit: {unit}")

    def solve(self) -> None:
        self._initialize_lp_variables()
        self._initialize_objective_variables()
        self._initialize_lp_problem()

        self._add_constraint_to_problem()
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
                * self._GRAM_CALCULATION_FACTOR
            )

            fat_ratio = (
                (self.total_fat * FAT_KCAL_PER_GRAM)
                / total_energy
                * self._GRAM_CALCULATION_FACTOR
            )

            carbohydrate_ratio = (
                (self.total_carbohydrates * CARBOHYDRATE_KCAL_PER_GRAM)
                / total_energy
                * self._GRAM_CALCULATION_FACTOR
            )

            print("### PFCバランス")
            print(f"たんぱく質割合: {protein_ratio:.1f}%")
            print(f"脂質割合: {fat_ratio:.1f}%")
            print(f"炭水化物割合: {carbohydrate_ratio:.1f}%")

        else:
            print("最適解が見つかりませんでした。")
