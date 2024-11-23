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
        self.problem: LpProblem

        # TODO: この辺は配列か辞書にまとめて簡単にしたいかも。
        self.total_energy: float = 0.0
        self.total_protein: float = 0.0
        self.total_fat: float = 0.0
        self.total_carbohydrates: float = 0.0

    def _setup_lp_variables(self) -> None:
        for food_item in self.foods:
            self.lp_variables[food_item.name] = LpVariable(
                food_item.name,
                lowBound=food_item.minimum_intake,
                upBound=food_item.maximum_intake,
                cat="Integer",
            )

    def _get_target_for_nutritional_component(
        self, nutritional_component: str
    ) -> float:
        if nutritional_component == "energy":
            return self.total_energy
        elif nutritional_component == "protein":
            return self.total_protein
        elif nutritional_component == "fat":
            return self.total_fat
        elif nutritional_component == "carbohydrates":
            return self.total_carbohydrates
        else:
            raise ValueError(
                f"Unknown nutritional component: {nutritional_component}"
            )

    def _setup_lp_problem(self) -> None:
        problem = self.objective.problem
        nutritional_component = self.objective.nutritional_component

        problem_sense = LpMinimize if problem == "minimize" else LpMaximize
        problem_name = f"{problem}_{nutritional_component}"

        self.problem = LpProblem(problem_name, problem_sense)

        problem_target = self._get_target_for_nutritional_component(
            nutritional_component
        )

        self.problem += (problem_target, f"{problem}_{nutritional_component}")

    def _setup_objective_variables(self) -> None:
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

    def _get_nutrient_value(self, nutritional_component: str) -> float:
        if nutritional_component == "energy":
            return self.total_energy
        elif nutritional_component == "protein":
            return self.total_protein
        elif nutritional_component == "fat":
            return self.total_fat
        elif nutritional_component == "carbohydrates":
            return self.total_carbohydrates
        else:
            raise ValueError(
                f"Unknown nutritional component: {nutritional_component}"
            )

    def _apply_amount_or_energy_constraint(
        self,
        min_max: str,
        nutrient_value: float,
        value: float,
        problem_name: str,
    ) -> None:
        if min_max == "max":
            self.problem += (nutrient_value <= value, problem_name)
        elif min_max == "min":
            self.problem += (nutrient_value >= value, problem_name)

    def _apply_fat_ratio_constraint(
        self, min_max: str, calculation_factor_value: float, problem_name: str
    ) -> None:
        total_fat_energy = self.total_fat * FoodInformation.FAT_ENERGY_PER_GRAM
        self._apply_nutrient_ratio_constraint(
            total_fat_energy, min_max, calculation_factor_value, problem_name
        )

    def _apply_protein_ratio_constraint(
        self, min_max: str, calculation_factor_value: float, problem_name: str
    ) -> None:
        total_protein_energy = (
            self.total_protein * FoodInformation.PROTEIN_ENERGY_PER_GRAM
        )
        self._apply_nutrient_ratio_constraint(
            total_protein_energy,
            min_max,
            calculation_factor_value,
            problem_name,
        )

    def _apply_carbohydrate_ratio_constraint(
        self, min_max: str, calculation_factor_value: float, problem_name: str
    ) -> None:
        total_carbohydrates_energy = (
            self.total_carbohydrates
            * FoodInformation.CARBOHYDRATES_ENERGY_PER_GRAM
        )
        self._apply_nutrient_ratio_constraint(
            total_carbohydrates_energy,
            min_max,
            calculation_factor_value,
            problem_name,
        )

    def _apply_nutrient_ratio_constraint(
        self,
        nutrient_energy: float,
        min_max: str,
        calculation_factor_value: float,
        problem_name: str,
    ) -> None:
        """栄養素のエネルギー割合制限を適用"""
        if min_max == "max":
            self.problem += (
                nutrient_energy
                <= self.total_energy * calculation_factor_value,
                problem_name,
            )
        elif min_max == "min":
            self.problem += (
                nutrient_energy
                >= self.total_energy * calculation_factor_value,
                problem_name,
            )

    def _apply_ratio_constraint(
        self,
        nutritional_component: str,
        min_max: str,
        calculation_factor_value: float,
        problem_name: str,
    ) -> None:
        """Ratio に基づく制約を適用"""
        if nutritional_component == "fat":
            self._apply_fat_ratio_constraint(
                min_max, calculation_factor_value, problem_name
            )
        elif nutritional_component == "protein":
            self._apply_protein_ratio_constraint(
                min_max, calculation_factor_value, problem_name
            )
        elif nutritional_component == "carbohydrates":
            self._apply_carbohydrate_ratio_constraint(
                min_max, calculation_factor_value, problem_name
            )
        else:
            raise ValueError(
                "Unknown nutritional component"
                f" for ratio: {nutritional_component}"
            )

    def _apply_constraint_for_unit(
        self,
        unit: str,
        nutritional_component: str,
        min_max: str,
        value: float,
        nutrient_value: float,
        problem_name: str,
        calculation_factor_value: float,
    ) -> None:
        """unitごとに制約を適用"""
        if unit in ["amount", "energy"]:
            self._apply_amount_or_energy_constraint(
                min_max, nutrient_value, value, problem_name
            )
        elif unit == "ratio":
            self._apply_ratio_constraint(
                nutritional_component,
                min_max,
                calculation_factor_value,
                problem_name,
            )
        else:
            raise ValueError(f"Unknown unit: {unit}")

    def _setup_constraints(self) -> None:
        # TODO: この辺がなんか長い。細分化したい。
        for constraint in self.constraints:
            nutritional_component = constraint.nutritional_component
            min_max = constraint.min_max
            value = constraint.value
            unit = constraint.unit

            nutrient_value = self._get_nutrient_value(nutritional_component)

            problem_name = f"{min_max}_{nutritional_component}_{unit}"
            calculation_factor_value = value / self._GRAM_CALCULATION_FACTOR
            # TODO: 画面側の表現を普通の単位に変えたいかも。Amount(g) とかじゃなくて g だけの方が直感的かも。
            self._apply_constraint_for_unit(
                unit,
                nutritional_component,
                min_max,
                value,
                nutrient_value,
                problem_name,
                calculation_factor_value,
            )

    def solve(self) -> dict:
        self._setup_lp_variables()
        self._setup_objective_variables()
        self._setup_lp_problem()
        self._setup_constraints()
        self.problem.solve()

        if LpStatus[self.problem.status] == "Optimal":
            result = {
                food: f"{self.lp_variables[food].varValue}g"
                for food in self.lp_variables
            }

            total_protein_value = sum(
                self.lp_variables[food].varValue * item.protein
                for food, item in zip(
                    self.lp_variables.keys(),
                    self.foods,
                )
            )

            total_fat_value = sum(
                self.lp_variables[food].varValue * item.fat
                for food, item in zip(
                    self.lp_variables.keys(),
                    self.foods,
                )
            )

            total_carbohydrate_value = sum(
                self.lp_variables[food].varValue * item.carbohydrates
                for food, item in zip(
                    self.lp_variables.keys(),
                    self.foods,
                )
            )

            total_kcal_value = (
                total_protein_value * FoodInformation.PROTEIN_ENERGY_PER_GRAM
                + total_fat_value * FoodInformation.FAT_ENERGY_PER_GRAM
                + total_carbohydrate_value
                * FoodInformation.CARBOHYDRATES_ENERGY_PER_GRAM
            )

            protein_ratio = (
                total_protein_value
                * FoodInformation.PROTEIN_ENERGY_PER_GRAM
                / total_kcal_value
            ) * self._GRAM_CALCULATION_FACTOR

            fat_ratio = (
                total_fat_value
                * FoodInformation.FAT_ENERGY_PER_GRAM
                / total_kcal_value
            ) * self._GRAM_CALCULATION_FACTOR

            carbohydrate_ratio = (
                total_carbohydrate_value
                * FoodInformation.CARBOHYDRATES_ENERGY_PER_GRAM
                / total_kcal_value
            ) * self._GRAM_CALCULATION_FACTOR

            pfc_ratio = {
                "protein_ratio": f"{protein_ratio:.1f}%",
                "fat_ratio": f"{fat_ratio:.1f}%",
                "carbohydrate_ratio": f"{carbohydrate_ratio:.1f}%",
            }

            return {
                "status": "Optimal",
                "result": result,
                "pfc_ratio": pfc_ratio,
            }
        else:
            return {"status": "Infeasible", "result": {}}
