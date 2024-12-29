from unittest.mock import MagicMock

import pytest
from flask import Request

from src.constraint import Constraint
from src.food_information import FoodInformation
from src.objective import Objective
from src.utilities import Utilities

_FOOD_INFORMATION_DATA = [
    {
        "name": "boiled_egg",
        "energy": 134,
        "protein": 12.5,
        "fat": 10.4,
        "carbohydrates": 0.3,
        "gramsPerUnit": 50,
        "minimumIntake": 1,
        "maximumIntake": 3,
    }
]

_OBJECTIVE_DATA = {
    "sense": "maximize",
    "nutrient": "energy",
}

_CONSTRAINTS_DATA = [
    {
        "minMax": "max",
        "nutrient": "energy",
        "unit": "energy",
        "value": 1800,
    },
    {
        "minMax": "min",
        "nutrient": "protein",
        "unit": "amount",
        "value": 150,
    },
]


def test_camel_to_snake() -> None:
    assert Utilities._camel_to_snake("camelToSnake") == "camel_to_snake"


def test_snake_to_camel() -> None:
    assert Utilities._snake_to_camel("snake_to_camel") == "snakeToCamel"


def test_parse_request_data() -> None:
    mock_request = MagicMock(spec=Request)
    mock_request.json = {
        "foodInformation": _FOOD_INFORMATION_DATA,
        "objective": _OBJECTIVE_DATA,
        "constraints": _CONSTRAINTS_DATA,
    }

    food_information, objective, constraints = Utilities.parse_request_data(
        mock_request
    )

    assert len(food_information) == 1
    assert isinstance(food_information, list)
    assert isinstance(food_information[0], FoodInformation)

    assert isinstance(objective, Objective)

    assert len(constraints) == 2
    assert isinstance(constraints, list)
    assert isinstance(constraints[0], Constraint)


def test_parse_invalid_request_data() -> None:
    mock_request = MagicMock(spec=Request)
    mock_request.json = None

    with pytest.raises(
        ValueError, match="Error processing request data: InvalidRequest"
    ):
        Utilities.parse_request_data(mock_request)


def test_convert_keys_to_camel_case() -> None:
    response = {"status": "Optimal", "food_intake": {"boiled_egg": 3}}
    result = Utilities.convert_keys_to_camel_case(response)

    assert "status" in result
    assert "foodIntake" in result
