from dataclasses import dataclass


@dataclass(frozen=True)
class FoodInformation:
    name: str
    energy: float
    protein: float
    fat: float
    carbohydrates: float
    # grams_per_unit: int
    minimum_intake: int
    maximum_intake: int

    PROTEIN_ENERGY_PER_GRAM = 4
    FAT_ENERGY_PER_GRAM = 9
    CARBOHYDRATES_ENERGY_PER_GRAM = 4

    def __post_init__(self) -> None:
        if any(
            x < 0
            for x in [self.energy, self.protein, self.fat, self.carbohydrates]
        ):
            raise ValueError(
                f"Invalid values for {self.name}"
                ", all nutrient values should be non-negative."
            )
