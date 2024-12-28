import re

import pytest

from src.objective import Objective


def test_valid_objective() -> None:
    objective = Objective(
        sense="maximize",
        nutrient="energy",
    )
    assert objective.sense == "maximize"
    assert objective.nutrient == "energy"


def test_invalid_objective_sense() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Invalid sense: invalid_sense."
            " Valid values are ['minimize', 'maximize']."
        ),
    ):
        Objective(
            sense="invalid_sense",
            nutrient="energy",
        )


def test_invalid_nutritional_component() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Invalid nutrient: invalid_nutrient. Valid nutrients are"
            " ['energy', 'protein', 'fat', 'carbohydrates']."
        ),
    ):
        Objective(
            sense="minimize",
            nutrient="invalid_nutrient",
        )
