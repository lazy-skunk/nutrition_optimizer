from dataclasses import dataclass

from src.food_information import FoodInformation


@dataclass(frozen=True)
class Objective:
    sense: str
    nutrient: str

    SENSES = ["minimize", "maximize"]

    def __post_init__(self) -> None:
        self._validate_sense()
        self._validate_nutrient()

    def _validate_sense(self) -> None:
        if self.sense not in self.SENSES:
            raise ValueError(
                f"Invalid sense: {self.sense}. Valid values are {self.SENSES}."
            )

    def _validate_nutrient(self) -> None:
        if self.nutrient not in FoodInformation.NUTRIENTS:
            raise ValueError(
                f"Invalid nutrient: {self.nutrient}."
                f" Valid nutrients are {FoodInformation.NUTRIENTS}."
            )
