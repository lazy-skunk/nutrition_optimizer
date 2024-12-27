import re

import pytest

from src.constraint import Constraint


def test_constraint_valid_input() -> None:
    constraint = Constraint(
        min_max="min",
        nutritional_component="protein",
        unit="amount",
        value=10,
    )

    assert constraint.min_max == "min"
    assert constraint.nutritional_component == "protein"
    assert constraint.unit == "amount"
    assert constraint.value == 10


def test_constraint_invalid_min_max() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Invalid Min/Max value: invalid_min_max."
            " Valid values are ['min', 'max']."
        ),
    ):
        Constraint(
            min_max="invalid_min_max",
            nutritional_component="protein",
            unit="amount",
            value=10,
        )


def test_constraint_invalid_nutritional_component() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Invalid nutritional component: invalid_component."
            " Valid components are"
            " ['energy', 'protein', 'fat', 'carbohydrates']."
        ),
    ):
        Constraint(
            min_max="min",
            nutritional_component="invalid_component",
            unit="amount",
            value=10,
        )


def test_constraint_invalid_unit() -> None:
    with pytest.raises(
        ValueError,
        match=re.escape(
            "Invalid unit: invalid_unit."
            " Valid units are ['amount', 'energy', 'ratio']."
        ),
    ):
        Constraint(
            min_max="min",
            nutritional_component="protein",
            unit="invalid_unit",
            value=10,
        )


def test_constraint_negative_value() -> None:
    with pytest.raises(
        ValueError, match="Constraint value must be non-negative. Got -1."
    ):
        Constraint(
            min_max="min",
            nutritional_component="protein",
            unit="amount",
            value=-1,
        )


def test_constraint_zero_value() -> None:
    constraint = Constraint(
        min_max="min",
        nutritional_component="protein",
        unit="amount",
        value=0,
    )
    assert constraint.value == 0
