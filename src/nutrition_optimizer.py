from pulp import LpMaximize, LpMinimize, LpProblem, LpStatus, LpVariable

from src.constraint import Constraint
from src.food_information import FoodInformation
from src.objective import Objective


class NutritionOptimizer:
    _GRAM_CALCULATION_FACTOR = 100

    def __init__(
        self,
        food_information: list[FoodInformation],
        objective: Objective,
        constraints: list[Constraint],
    ) -> None:
        self.food_information: list[FoodInformation] = food_information
        self.objective: Objective = objective
        self.constraints: list[Constraint] = constraints

        self.food_intake_variables: dict[str, LpVariable] = {}
        self.problem: LpProblem

        # TODO: この辺は配列か辞書にまとめて簡単にしたいかも。
        self.total_energy: float = 0.0
        self.total_protein: float = 0.0
        self.total_fat: float = 0.0
        self.total_carbohydrates: float = 0.0

    def _setup_food_intake_variables(self) -> None:
        for food_infomation in self.food_information:
            self.food_intake_variables[food_infomation.name] = LpVariable(
                food_infomation.name,
                lowBound=food_infomation.minimum_intake,
                upBound=food_infomation.maximum_intake,
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

        problem_sense = LpMaximize if problem == "maximize" else LpMinimize
        problem_name = f"{problem}_{nutritional_component}"

        self.problem = LpProblem(problem_name, problem_sense)

        problem_target = self._get_target_for_nutritional_component(
            nutritional_component
        )

        self.problem += problem_target, problem_name

    def _setup_objective_variables(self) -> None:
        for food_information in self.food_information:
            self.total_energy += (
                food_information.energy
                * food_information.grams_per_unit
                * self.food_intake_variables[food_information.name]
                / self._GRAM_CALCULATION_FACTOR
            )

            self.total_protein += (
                food_information.protein
                * food_information.grams_per_unit
                * self.food_intake_variables[food_information.name]
                / self._GRAM_CALCULATION_FACTOR
            )

            self.total_fat += (
                food_information.fat
                * food_information.grams_per_unit
                * self.food_intake_variables[food_information.name]
                / self._GRAM_CALCULATION_FACTOR
            )

            self.total_carbohydrates += (
                food_information.carbohydrates
                * food_information.grams_per_unit
                * self.food_intake_variables[food_information.name]
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

    def _apply_nutrient_ratio_constraint(
        self,
        nutrient_energy: float,
        min_max: str,
        calculation_factor_value: float,
        problem_name: str,
    ) -> None:
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

    def _apply_ratio_constraint(
        self,
        nutritional_component: str,
        min_max: str,
        calculation_factor_value: float,
        problem_name: str,
    ) -> None:
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
                f"Unknown nutritional component: {nutritional_component}"
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
        for constraint in self.constraints:
            nutritional_component = constraint.nutritional_component
            min_max = constraint.min_max
            value = constraint.value
            unit = constraint.unit

            nutrient_value = self._get_nutrient_value(nutritional_component)

            problem_name = f"{min_max}_{nutritional_component}_{unit}"
            calculation_factor_value = value / self._GRAM_CALCULATION_FACTOR
            # TODO: 画面側の表現を普通の単位に変えたいかも。Amount(g) とかじゃなくて g だけの方が直感的かも。
            # TODO: 引数を減らせないか検討したい。
            self._apply_constraint_for_unit(
                unit,
                nutritional_component,
                min_max,
                value,
                nutrient_value,
                problem_name,
                calculation_factor_value,
            )

    def _calculate_total_nutrients(self) -> tuple[float, float, float, float]:
        total_protein_value = sum(
            item.protein
            * item.grams_per_unit
            * self.food_intake_variables[food].varValue
            / self._GRAM_CALCULATION_FACTOR
            for food, item in zip(
                self.food_intake_variables.keys(), self.food_information
            )
        )

        total_fat_value = sum(
            self.food_intake_variables[food].varValue
            * item.grams_per_unit
            * item.fat
            / self._GRAM_CALCULATION_FACTOR
            for food, item in zip(
                self.food_intake_variables.keys(), self.food_information
            )
        )

        total_carbohydrate_value = sum(
            self.food_intake_variables[food].varValue
            * item.grams_per_unit
            * item.carbohydrates
            / self._GRAM_CALCULATION_FACTOR
            for food, item in zip(
                self.food_intake_variables.keys(), self.food_information
            )
        )

        total_kcal_value = sum(
            self.food_intake_variables[food].varValue
            * item.grams_per_unit
            * item.energy
            / self._GRAM_CALCULATION_FACTOR
            for food, item in zip(
                self.food_intake_variables.keys(), self.food_information
            )
        )

        return (
            total_protein_value,
            total_fat_value,
            total_carbohydrate_value,
            total_kcal_value,
        )

    def _calculate_pfc_ratios(
        self,
        total_protein_value: float,
        total_fat_value: float,
        total_carbohydrate_value: float,
        total_kcal_value: float,
    ) -> dict:
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

        return {
            "protein_ratio": protein_ratio,
            "fat_ratio": fat_ratio,
            "carbohydrate_ratio": carbohydrate_ratio,
        }

    def _calculate_food_intake(self) -> dict:
        food_intake = {
            food: self.food_intake_variables[food].varValue
            for food in self.food_intake_variables
        }
        return food_intake

    def solve(self) -> dict:
        self._setup_food_intake_variables()
        self._setup_objective_variables()
        self._setup_lp_problem()
        self._setup_constraints()
        self.problem.solve()

        solution_result = LpStatus[self.problem.status]
        if solution_result == "Optimal":
            food_intake = self._calculate_food_intake()

            (
                total_protein_value,
                total_fat_value,
                total_carbohydrate_value,
                total_kcal_value,
            ) = self._calculate_total_nutrients()

            pfc_kcal_values = {
                "protein": total_protein_value,
                "fat": total_fat_value,
                "carbohydrates": total_carbohydrate_value,
                "kcal": total_kcal_value,
            }

            pfc_ratio = self._calculate_pfc_ratios(
                total_protein_value,
                total_fat_value,
                total_carbohydrate_value,
                total_kcal_value,
            )

            return {
                "status": solution_result,
                "food_intake": food_intake,
                "pfc_ratio": pfc_ratio,
                "pfc_kcal_values": pfc_kcal_values,
            }
        else:
            return {"status": solution_result}
