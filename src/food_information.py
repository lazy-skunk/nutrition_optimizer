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
        if any(
            x < 0
            for x in [self.energy, self.protein, self.fat, self.carbohydrates]
        ):
            raise ValueError(
                f"Invalid values for {self.name}"
                ", all nutrient values should be non-negative."
            )
