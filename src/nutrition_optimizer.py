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

    def _get_problem_target(self, nutritional_component: str) -> float:
        return getattr(self, f"total_{nutritional_component}")

    def _setup_lp_problem(self) -> None:
        problem = self.objective.problem
        nutritional_component = self.objective.nutritional_component

        # TODO: problem の値で getattr したいかも。
        problem_sense = LpMaximize if problem == "maximize" else LpMinimize
        problem_name = f"{problem}_{nutritional_component}"

        self.problem = LpProblem(problem_name, problem_sense)

        problem_target = self._get_problem_target(nutritional_component)

        self.problem += problem_target, problem_name

    def _setup_objective_variables(self) -> None:
        for food_information in self.food_information:
            for nutrient in FoodInformation.NUTRIENT_COMPONENTS:
                nutrient_value = getattr(food_information, nutrient)

                total_value = (
                    nutrient_value
                    * food_information.grams_per_unit
                    * self.food_intake_variables[food_information.name]
                    / self._GRAM_CALCULATION_FACTOR
                )

                nutrient_attribute = f"total_{nutrient}"
                setattr(
                    self,
                    nutrient_attribute,
                    getattr(self, nutrient_attribute) + total_value,
                )

    def _get_nutrient_value(self, nutritional_component: str) -> float:
        return getattr(self, f"total_{nutritional_component}")

    def _apply_amount_or_energy_constraint(
        self,
        constraint: Constraint,
    ) -> None:
        nutrient_value = self._get_nutrient_value(
            constraint.nutritional_component
        )
        min_max = constraint.min_max
        nutritional_component = constraint.nutritional_component
        unit = constraint.unit
        value = constraint.value

        problem_name = f"{min_max}_{nutritional_component}_{unit}"

        if min_max == "max":
            self.problem += (nutrient_value <= value, problem_name)
        elif min_max == "min":
            self.problem += (nutrient_value >= value, problem_name)

    def _apply_ratio_constraint_for_nutrient(
        self,
        constraint: Constraint,
        nutrient_energy: float,
    ) -> None:
        min_max = constraint.min_max
        nutritional_component = constraint.nutritional_component
        unit = constraint.unit

        problem_name = f"{min_max}_{nutritional_component}_{unit}"

        calculation_factor_value = (
            constraint.value / self._GRAM_CALCULATION_FACTOR
        )

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
        constraint: Constraint,
    ) -> None:
        nutritional_component = constraint.nutritional_component

        if nutritional_component == "fat":
            total_fat_energy = (
                self.total_fat * FoodInformation.FAT_ENERGY_PER_GRAM
            )
            self._apply_ratio_constraint_for_nutrient(
                constraint, total_fat_energy
            )
        elif nutritional_component == "protein":
            total_protein_energy = (
                self.total_protein * FoodInformation.PROTEIN_ENERGY_PER_GRAM
            )
            self._apply_ratio_constraint_for_nutrient(
                constraint, total_protein_energy
            )
        elif nutritional_component == "carbohydrates":
            total_carbohydrates_energy = (
                self.total_carbohydrates
                * FoodInformation.CARBOHYDRATES_ENERGY_PER_GRAM
            )
            self._apply_ratio_constraint_for_nutrient(
                constraint, total_carbohydrates_energy
            )
        else:
            raise ValueError(
                f"Unknown nutritional component: {nutritional_component}"
            )

    def _setup_constraints(self) -> None:
        for constraint in self.constraints:
            # TODO: 画面側の表現を普通の単位に変えたいかも。Amount(g) とかじゃなくて g だけの方が直感的かも。
            unit = constraint.unit
            if unit in ["amount", "energy"]:
                self._apply_amount_or_energy_constraint(constraint)
            elif unit == "ratio":
                self._apply_ratio_constraint(constraint)
            else:
                raise ValueError(f"Unknown unit: {unit}")

    def _calculate_total_nutrients(self, nutrient_property: str) -> float:
        return sum(
            getattr(food_information, nutrient_property)
            * food_information.grams_per_unit
            * self.food_intake_variables[food_name].varValue
            / self._GRAM_CALCULATION_FACTOR
            for food_name, food_information in zip(
                self.food_intake_variables.keys(), self.food_information
            )
        )

    def _calculate_pfc_ratios(
        self,
        total_protein_value: float,
        total_fat_value: float,
        total_carbohydrate_value: float,
        total_kcal_value: float,
    ) -> dict:
        # TODO: おや？ここも改良できるな。冗長だ。
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
            food_name: self.food_intake_variables[food_name].varValue
            for food_name in self.food_intake_variables
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

            total_protein_value = self._calculate_total_nutrients("protein")
            total_fat_value = self._calculate_total_nutrients("fat")
            total_carbohydrate_value = self._calculate_total_nutrients(
                "carbohydrates"
            )
            total_kcal_value = self._calculate_total_nutrients("energy")

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
