from dataclasses import dataclass

from src.food_information import FoodInformation
from src.singleton_logger import SingletonLogger

_logger = SingletonLogger.get_logger()


@dataclass(frozen=True)
class Constraint:
    min_max: str
    nutritional_component: str
    unit: str
    value: int

    MIN_MAX = ["min", "max"]
    UNITS = ["amount", "energy", "ratio"]

    def __post_init__(self) -> None:
        _logger.debug(
            f"Initializing Constraint with min_max={self.min_max},"
            f" nutritional_component={self.nutritional_component},"
            f" unit={self.unit}, value={self.value}"
        )
        self._validate_min_max()
        self._validate_nutritional_component()
        self._validate_unit()
        self._validate_value_is_non_negative()

    def _validate_min_max(self) -> None:
        if self.min_max not in self.MIN_MAX:
            error_message = (
                f"Invalid Min/Max value: {self.min_max}."
                f" Valid values are {Constraint.MIN_MAX}."
            )
            _logger.error(error_message)
            raise ValueError(error_message)
        _logger.info(f"Min/Max value '{self.min_max}' is valid.")

    def _validate_nutritional_component(self) -> None:
        if (
            self.nutritional_component
            not in FoodInformation.NUTRIENT_COMPONENTS
        ):
            error_message = (
                f"Invalid nutritional component: {self.nutritional_component}."
                f" Valid components are {FoodInformation.NUTRIENT_COMPONENTS}."
            )
            _logger.error(error_message)
            raise ValueError(error_message)

        _logger.info(
            f"Nutritional component '{self.nutritional_component}' is valid."
        )

    def _validate_unit(self) -> None:
        if self.unit not in self.UNITS:
            error_message = (
                f"Invalid unit: {self.unit}."
                f" Valid units are {Constraint.UNITS}."
            )
            _logger.error(error_message)
            raise ValueError(error_message)

        _logger.info(f"Unit '{self.unit}' is valid.")

    def _validate_value_is_non_negative(self) -> None:
        if self.value is None or self.value < 0:
            error_message = (
                f"Constraint value must be non-negative. Got {self.value}."
            )
            _logger.error(error_message)
            raise ValueError(error_message)

        _logger.info(f"Value '{self.value}' is valid and non-negative.")
