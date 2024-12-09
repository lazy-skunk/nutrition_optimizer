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

    def _get_nutrient_value(self, nutritional_component: str) -> float:
        nutrient_attribute = f"total_{nutritional_component}"
        return getattr(self, nutrient_attribute)

    def _setup_lp_problem(self) -> None:
        problem = self.objective.problem
        nutritional_component = self.objective.nutritional_component

        # TODO: problem の値で getattr したいかも。
        # problem_sense = getattr(pulp, problem)
        problem_sense = LpMaximize if problem == "maximize" else LpMinimize
        problem_name = f"{problem}_{nutritional_component}"

        self.problem = LpProblem(problem_name, problem_sense)

        problem_target = self._get_nutrient_value(nutritional_component)

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
                current_value = getattr(self, nutrient_attribute)
                setattr(
                    self,
                    nutrient_attribute,
                    current_value + total_value,
                )

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

        constraint_operations = {
            "max": lambda nutrient_value, value: nutrient_value <= value,
            "min": lambda nutrient_value, value: nutrient_value >= value,
        }
        constraint_operation = constraint_operations[min_max]

        self.problem += (
            constraint_operation(nutrient_value, value),
            problem_name,
        )

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

        comparison_operations = {
            "max": lambda nutrient_energy: nutrient_energy
            <= self.total_energy * calculation_factor_value,
            "min": lambda nutrient_energy: nutrient_energy
            >= self.total_energy * calculation_factor_value,
        }
        comparison_operation = comparison_operations[min_max]

        self.problem += (
            comparison_operation(nutrient_energy),
            problem_name,
        )

    def _apply_ratio_constraint(
        self,
        constraint: Constraint,
    ) -> None:
        nutritional_component = constraint.nutritional_component
        total_nutrient_value = self._get_nutrient_value(nutritional_component)

        nutrient_energy_per_gram_attribute = (
            f"{nutritional_component.upper()}_ENERGY_PER_GRAM"
        )
        nutrient_energy_per_gram = getattr(
            FoodInformation, nutrient_energy_per_gram_attribute
        )

        total_nutrient_energy = total_nutrient_value * nutrient_energy_per_gram

        self._apply_ratio_constraint_for_nutrient(
            constraint, total_nutrient_energy
        )

    def _setup_constraints(self) -> None:
        apply_methods = {
            "amount": self._apply_amount_or_energy_constraint,
            "energy": self._apply_amount_or_energy_constraint,
            "ratio": self._apply_ratio_constraint,
        }
        for constraint in self.constraints:
            # TODO: 画面側の表現を普通の単位に変えたいかも。Amount(g) とかじゃなくて g だけの方が直感的かも。
            unit = constraint.unit
            apply_method = apply_methods[unit]
            apply_method(constraint)

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

    def _calculate_food_intake(self) -> dict:
        food_intake = {
            food_name: self.food_intake_variables[food_name].varValue
            for food_name in self.food_intake_variables
        }
        return food_intake

    def _calculate_total_nutrient_values(self) -> dict:
        total_values = {}

        for nutrient_component in FoodInformation.NUTRIENT_COMPONENTS:
            total_values[nutrient_component] = self._calculate_total_nutrients(
                nutrient_component
            )

        return total_values

    def _calculate_pfc_ratios(self, total_values: dict) -> dict:
        pfc_ratios = {}
        total_energy_value = total_values["energy"]

        for nutrient_component in FoodInformation.NUTRIENT_COMPONENTS:
            if nutrient_component == "energy":
                continue

            total_nutrient_value = total_values[nutrient_component]

            energy_per_gram_attribute = (
                f"{nutrient_component.upper()}_ENERGY_PER_GRAM"
            )
            energy_per_gram = getattr(
                FoodInformation,
                energy_per_gram_attribute,
            )

            ratio = (
                total_nutrient_value * energy_per_gram / total_energy_value
            ) * self._GRAM_CALCULATION_FACTOR

            pfc_ratios[nutrient_component] = ratio

        return pfc_ratios

    def solve(self) -> dict:
        self._setup_food_intake_variables()
        self._setup_objective_variables()
        self._setup_lp_problem()
        self._setup_constraints()
        self.problem.solve()

        solution_result = LpStatus[self.problem.status]
        if solution_result == "Optimal":
            food_intake = self._calculate_food_intake()
            pfc_kcal_total_values = self._calculate_total_nutrient_values()
            pfc_ratio = self._calculate_pfc_ratios(pfc_kcal_total_values)

            return {
                "status": solution_result,
                "food_intake": food_intake,
                "pfc_kcal_total_values": pfc_kcal_total_values,
                "pfc_ratio": pfc_ratio,
            }
        else:
            return {"status": solution_result}
