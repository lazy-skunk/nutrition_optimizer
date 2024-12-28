from pulp import (
    LpInteger,
    LpMaximize,
    LpMinimize,
    LpProblem,
    LpStatus,
    LpVariable,
)

from src.constraint import Constraint
from src.food_information import FoodInformation
from src.objective import Objective
from src.singleton_logger import SingletonLogger


class NutritionOptimizer:
    _GRAM_CALCULATION_FACTOR = 100

    def __init__(
        self,
        food_information: list[FoodInformation],
        objective: Objective,
        constraints: list[Constraint],
    ) -> None:
        self._food_information: list[FoodInformation] = food_information
        self._objective: Objective = objective
        self._constraints: list[Constraint] = constraints

        self._logger = SingletonLogger.get_logger()

        self._food_intake_variables: dict[str, LpVariable] = {}
        self._problem: LpProblem

        # TODO: 目的変数であることをがわかるような工夫が必要かもしれない。
        self._total_energy: float = 0.0
        self._total_protein: float = 0.0
        self._total_fat: float = 0.0
        self._total_carbohydrates: float = 0.0

    def _setup_food_intake_variables(self) -> None:
        self._logger.info("Setting up food intake variables.")

        for food_infomation in self._food_information:
            self._food_intake_variables[food_infomation.name] = LpVariable(
                food_infomation.name,
                lowBound=food_infomation.minimum_intake,
                upBound=food_infomation.maximum_intake,
                cat=LpInteger,
            )

        self._logger.info("Completed setting up food intake variables.")

    def _get_objective_variable(self, nutrient: str) -> float:
        nutrient_attribute = f"_total_{nutrient}"
        return getattr(self, nutrient_attribute)

    def _setup_lp_problem(self) -> None:
        self._logger.info("Setting up LP problem.")

        sense = self._objective.sense
        objective = LpMaximize if sense == "maximize" else LpMinimize

        nutrient = self._objective.nutrient
        objective_name = f"{sense}_{nutrient}"

        self._problem = LpProblem(objective_name, objective)

        objective_target = self._get_objective_variable(nutrient)
        self._problem += objective_target, objective_name

        self._logger.info("Completed setting up LP problem.")

    def _update_objective_variable(
        self, nutrient: str, objective_variables: float
    ) -> None:
        nutrient_attribute = f"_total_{nutrient}"
        setattr(self, nutrient_attribute, objective_variables)

    def _setup_objective_variables(self) -> None:
        self._logger.info("Setting up objective variables.")

        for food_information in self._food_information:
            for nutrient in FoodInformation.NUTRIENTS:
                nutrient_value = getattr(food_information, nutrient)

                objective_variable = (
                    nutrient_value
                    * food_information.grams_per_unit
                    * self._food_intake_variables[food_information.name]
                    / self._GRAM_CALCULATION_FACTOR
                )

                current_objective_variables = self._get_objective_variable(
                    nutrient
                )
                new_objective_variables = (
                    current_objective_variables + objective_variable
                )

                self._update_objective_variable(
                    nutrient, new_objective_variables
                )

        self._logger.info("Completed setting up objective variables.")

    def _apply_amount_or_energy_constraint(
        self,
        constraint: Constraint,
    ) -> None:
        constraint_operations = {
            "max": lambda objective_variable, value: objective_variable
            <= value,
            "min": lambda objective_variable, value: objective_variable
            >= value,
        }
        min_max = constraint.min_max
        constraint_operation = constraint_operations[min_max]

        nutrient = constraint.nutrient
        objective_variable = self._get_objective_variable(nutrient)

        value = constraint.value

        unit = constraint.unit
        constraint_name = f"{min_max}_{nutrient}_{unit}"

        self._problem += (
            constraint_operation(objective_variable, value),
            constraint_name,
        )

    def _get_nutrient_energy_per_gram(self, nutrient: str) -> int:
        nutrient_energy_per_gram_attribute = (
            f"{nutrient.upper()}_ENERGY_PER_GRAM"
        )
        return getattr(FoodInformation, nutrient_energy_per_gram_attribute)

    def _apply_ratio_constraint(
        self,
        constraint: Constraint,
    ) -> None:
        nutrient = constraint.nutrient
        objective_variable = self._get_objective_variable(nutrient)
        nutrient_energy_per_gram = self._get_nutrient_energy_per_gram(nutrient)
        total_nutrient_energy = objective_variable * nutrient_energy_per_gram

        min_max = constraint.min_max
        unit = constraint.unit
        constraint_name = f"{min_max}_{nutrient}_{unit}"

        value = constraint.value
        calculation_factor = value / self._GRAM_CALCULATION_FACTOR

        comparison_operations = {
            "max": lambda nutrient_energy: nutrient_energy
            <= self._total_energy * calculation_factor,
            "min": lambda nutrient_energy: nutrient_energy
            >= self._total_energy * calculation_factor,
        }
        comparison_operation = comparison_operations[min_max]

        self._problem += (
            comparison_operation(total_nutrient_energy),
            constraint_name,
        )

    def _setup_constraints(self) -> None:
        self._logger.info("Setting up constraints.")

        apply_methods = {
            "amount": self._apply_amount_or_energy_constraint,
            "energy": self._apply_amount_or_energy_constraint,
            "ratio": self._apply_ratio_constraint,
        }
        for constraint in self._constraints:
            unit = constraint.unit
            apply_method = apply_methods[unit]
            apply_method(constraint)

        self._logger.info("Completed setting up constraints.")

    def _calculate_food_intakes(self) -> dict:
        return {
            food_name: self._food_intake_variables[food_name].varValue
            for food_name in self._food_intake_variables
        }

    def _calculate_total_nutrient_values(self) -> dict:
        total_nutrient_values = {}

        for nutrient in FoodInformation.NUTRIENTS:
            total_nutrient_value = sum(
                getattr(food_information, nutrient)
                * food_information.grams_per_unit
                * self._food_intake_variables[food_name].varValue
                / self._GRAM_CALCULATION_FACTOR
                for food_name, food_information in zip(
                    self._food_intake_variables.keys(),
                    self._food_information,
                )
            )
            rounded_nutrient_value = round(total_nutrient_value, 1)
            total_nutrient_values[nutrient] = rounded_nutrient_value

        return total_nutrient_values

    def _recalculate_total_energy(self, total_values: dict) -> float:
        recalculated_total_energy = 0

        for nutrient in FoodInformation.NUTRIENTS:
            if nutrient == "energy":
                continue

            energy_per_gram = self._get_nutrient_energy_per_gram(nutrient)
            recalculated_total_energy += (
                total_values[nutrient] * energy_per_gram
            )

        return recalculated_total_energy

    def _calculate_pfc_ratio(self, total_nutrient_values: dict) -> dict:
        pfc_ratio = {}

        recalculated_total_energy = self._recalculate_total_energy(
            total_nutrient_values
        )

        for nutrient_component in FoodInformation.NUTRIENTS:
            if nutrient_component == "energy":
                continue

            total_nutrient_value = total_nutrient_values[nutrient_component]
            energy_per_gram = self._get_nutrient_energy_per_gram(
                nutrient_component
            )

            ratio = (
                total_nutrient_value
                * energy_per_gram
                / recalculated_total_energy
            ) * self._GRAM_CALCULATION_FACTOR
            rounded_ratio = round(ratio, 1)
            pfc_ratio[nutrient_component] = rounded_ratio

        return pfc_ratio

    def _preparation(self) -> None:
        self._logger.info("Starting preparation for solve.")

        self._setup_food_intake_variables()
        self._setup_objective_variables()
        self._setup_lp_problem()
        self._setup_constraints()

        self._logger.info("Completed preparation for solve.")

    def solve(self) -> dict:
        self._preparation()

        self._logger.info("Starting to solve the optimization problem.")
        self._problem.solve()

        solution_result = LpStatus[self._problem.status]
        if solution_result == "Optimal":
            self._logger.info("Optimization completed successfully.")

            food_intakes = self._calculate_food_intakes()
            total_nutrient_values = self._calculate_total_nutrient_values()
            pfc_ratio = self._calculate_pfc_ratio(total_nutrient_values)

            return {
                "status": solution_result,
                "food_intakes": food_intakes,
                "total_nutrient_values": total_nutrient_values,
                "pfc_ratio": pfc_ratio,
            }
        else:
            self._logger.warning(
                f"Optimization failed with status: {solution_result}"
            )
            return {
                "status": solution_result,
                "message": "Please review the constraints,"
                " the grams per unit, or the intake values.",
            }
