from dataclasses import dataclass


@dataclass(frozen=True)
class FoodInformation:
    name: str
    energy: float
    protein: float
    fat: float
    carbohydrates: float

    minimum_intake: int
    maximum_intake: int
    # TODO: 1個当たりのグラム数は画面から入力できるように調整すること。
    grams_per_unit: int = 1

    PROTEIN_ENERGY_PER_GRAM = 4
    FAT_ENERGY_PER_GRAM = 9
    CARBOHYDRATES_ENERGY_PER_GRAM = 4

    def __post_init__(self) -> None:
        self._validate_nutrient_values_are_non_negative()
        self._validate_grams_per_unit_is_greater_than_zero()
        self._validate_intake_values_are_non_negative()
        self._validate_minimum_intake_is_less_than_maximum_intake()

    def _validate_nutrient_values_are_non_negative(self) -> None:
        if any(
            value < 0
            for value in [
                self.energy,
                self.protein,
                self.fat,
                self.carbohydrates,
            ]
        ):
            raise ValueError(
                f"Invalid values for {self.name}."
                " All nutrient values must be non-negative."
            )

    def _validate_grams_per_unit_is_greater_than_zero(self) -> None:
        if self.grams_per_unit > 0:
            raise ValueError(
                f"Invalid grams_per_unit for {self.name}."
                " It must be greater than zero."
            )

    def _validate_intake_values_are_non_negative(self) -> None:
        if self.minimum_intake < 0 or self.maximum_intake < 0:
            raise ValueError(
                f"Invalid intake values for {self.name}."
                " Both minimum_intake and maximum_intake must be non-negative."
            )

    def _validate_minimum_intake_is_less_than_maximum_intake(self) -> None:
        if not self.minimum_intake < self.maximum_intake:
            raise ValueError(
                f"Invalid intake range for {self.name}."
                " Maximum_intake must be greater than minimum_intake."
            )
