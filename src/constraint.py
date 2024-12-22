from dataclasses import dataclass

from src.food_information import FoodInformation


@dataclass(frozen=True)
class Constraint:
    min_max: str
    nutritional_component: str
    unit: str
    value: int

    MIN_MAX = ["min", "max"]
    UNITS = ["amount", "energy", "ratio"]

    def __post_init__(self) -> None:
        self._validate_min_max()
        self._validate_nutritional_component()
        self._validate_unit()
        self._validate_value_is_non_negative()

    def _validate_min_max(self) -> None:
        if self.min_max not in self.MIN_MAX:
            raise ValueError(
                f"Invalid min_max value: {self.min_max}."
                " Valid values are 'min' or 'max'."
            )

    def _validate_nutritional_component(self) -> None:
        if (
            self.nutritional_component
            not in FoodInformation.NUTRIENT_COMPONENTS
        ):
            raise ValueError(
                f"Invalid nutritional_component: {self.nutritional_component}."
                f" Valid components are {FoodInformation.NUTRIENT_COMPONENTS}."
            )

    def _validate_unit(self) -> None:
        if self.unit not in self.UNITS:
            raise ValueError(
                f"Invalid unit: {self.unit}."
                " Valid units are 'amount', 'energy', or 'ratio'."
            )

    def _validate_value_is_non_negative(self) -> None:
        if self.value is None or self.value < 0:
            raise ValueError(f"Value must be non-negative. Got {self.value}.")
