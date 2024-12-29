import pytest

from src.food_information import FoodInformation


def test_valid_food_information() -> None:
    boiled_egg = FoodInformation(
        name="boiled_egg",
        energy=134,
        protein=12.5,
        fat=10.4,
        carbohydrates=0.3,
        grams_per_unit=50,
        minimum_intake=1,
        maximum_intake=3,
    )

    assert boiled_egg.name == "boiled_egg"
    assert boiled_egg.energy == 134
    assert boiled_egg.protein == 12.5
    assert boiled_egg.fat == 10.4
    assert boiled_egg.carbohydrates == 0.3
    assert boiled_egg.grams_per_unit == 50
    assert boiled_egg.minimum_intake == 1
    assert boiled_egg.maximum_intake == 3


def test_blank_name() -> None:
    with pytest.raises(ValueError, match="Food name must be provided."):
        FoodInformation(
            name=" ",  # Blank
            energy=134,
            protein=12.5,
            fat=10.4,
            carbohydrates=0.3,
            grams_per_unit=50,
            minimum_intake=1,
            maximum_intake=3,
        )


def test_negative_nutrient_values() -> None:
    nutrients = ["energy", "protein", "fat", "carbohydrates"]
    for nutrient in nutrients:
        with pytest.raises(
            ValueError,
            match="Invalid values for boiled_egg."
            " All nutrient values must be non-negative.",
        ):
            FoodInformation(
                name="boiled_egg",
                energy=-134 if nutrient == "energy" else 134,
                protein=-12.5 if nutrient == "protein" else 12.5,
                fat=-10.4 if nutrient == "fat" else 10.4,
                carbohydrates=-0.3 if nutrient == "carbohydrates" else 0.3,
                grams_per_unit=50,
                minimum_intake=1,
                maximum_intake=3,
            )


def test_invalid_grams_per_unit() -> None:
    with pytest.raises(
        ValueError,
        match="Invalid grams per unit for boiled_egg."
        " It must be greater than zero.",
    ):
        FoodInformation(
            name="boiled_egg",
            energy=134,
            protein=12.5,
            fat=10.4,
            carbohydrates=0.3,
            grams_per_unit=0,  # Zero
            minimum_intake=1,
            maximum_intake=3,
        )


def test_negative_intake_values() -> None:
    negative_intake_values = [
        (-1, 3),
        (1, -3),
    ]

    for minimum_intake, maximum_intake in negative_intake_values:
        with pytest.raises(
            ValueError,
            match="Both minimum_intake"
            " and maximum_intake must be non-negative.",
        ):
            FoodInformation(
                name="boiled_egg",
                energy=134,
                protein=12.5,
                fat=10.4,
                carbohydrates=0.3,
                grams_per_unit=50,
                minimum_intake=minimum_intake,
                maximum_intake=maximum_intake,
            )


def test_minimum_intake_is_less_than_maximum_intake() -> None:
    with pytest.raises(
        ValueError, match="Maximum_intake must be greater than minimum_intake."
    ):
        FoodInformation(
            name="boiled_egg",
            energy=134,
            protein=12.5,
            fat=10.4,
            carbohydrates=0.3,
            grams_per_unit=50,
            minimum_intake=3,  # Greater than maximum_intake
            maximum_intake=1,
        )
