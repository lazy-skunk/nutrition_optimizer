import re

import pytest

from src.objective import Objective


def test_valid_objective() -> None:
    objective = Objective(
        objective_sense="maximize",
        nutritional_component="energy",
    )
    assert objective.objective_sense == "maximize"
    assert objective.nutritional_component == "energy"


def test_invalid_objective_sense() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Invalid objective sense: invalid_sense."
            " Valid values are ['minimize', 'maximize']."
        ),
    ):
        Objective(
            objective_sense="invalid_sense",
            nutritional_component="energy",
        )


def test_invalid_nutritional_component() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Invalid nutritional component: invalid_component."
            " Valid components are"
            " ['energy', 'protein', 'fat', 'carbohydrates']."
        ),
    ):
        Objective(
            objective_sense="minimize",
            nutritional_component="invalid_component",
        )
