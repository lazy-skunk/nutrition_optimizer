from dataclasses import dataclass

from src.food_information import FoodInformation


@dataclass(frozen=True)
class Objective:
    objective_sense: str
    nutritional_component: str

    OBJECTIVE_SENSES = ["minimize", "maximize"]

    def __post_init__(self) -> None:
        self._validate_problem_type()
        self._validate_nutritional_component()

    def _validate_problem_type(self) -> None:
        if self.objective_sense not in self.OBJECTIVE_SENSES:
            raise ValueError(
                f"Invalid objective sense: {self.objective_sense}."
                f" Valid values are {self.OBJECTIVE_SENSES}."
            )

    def _validate_nutritional_component(self) -> None:
        if (
            self.nutritional_component
            not in FoodInformation.NUTRIENT_COMPONENTS
        ):
            raise ValueError(
                f"Invalid nutritional component: {self.nutritional_component}."
                f" Valid components are {FoodInformation.NUTRIENT_COMPONENTS}."
            )
