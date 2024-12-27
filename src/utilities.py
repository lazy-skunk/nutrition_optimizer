import re
from typing import Type

from flask import Request

from src.constraint import Constraint
from src.food_information import FoodInformation
from src.objective import Objective


class Utilities:
    @staticmethod
    def _camel_to_snake(camel_case_str: str) -> str:
        CAMEL_TO_SNAKE_PATTERN = r"([a-z])([A-Z])"
        REPLACEMENT_STRING = r"\1_\2"

        snake_case_str = re.sub(
            CAMEL_TO_SNAKE_PATTERN, REPLACEMENT_STRING, camel_case_str
        ).lower()

        return snake_case_str

    @staticmethod
    def _snake_to_camel(snake_case_str: str) -> str:
        SNAKE = "_"

        words = snake_case_str.split(SNAKE)
        return "".join(
            word.capitalize() if word_count != 0 else word
            for word_count, word in enumerate(words)
        )

    @staticmethod
    def _convert_to_generic(data: list, cls: Type) -> list:
        return [
            cls(
                **{
                    Utilities._camel_to_snake(key): value
                    for key, value in item.items()
                }
            )
            for item in data
        ]

    @staticmethod
    def _convert_to_objective(data: dict) -> Objective:
        return Objective(
            **{
                Utilities._camel_to_snake(key): value
                for key, value in data.items()
            }
        )

    @staticmethod
    def parse_request_data(request: Request) -> tuple:
        try:
            if request is None or request.json is None:
                raise ValueError(
                    "Error processing request data: InvalidRequest"
                )

            food_information_request = request.json.get("foodInformation")
            food_information = Utilities._convert_to_generic(
                food_information_request, FoodInformation
            )

            objective_request = request.json.get("objective")
            objective = Utilities._convert_to_objective(objective_request)

            constraints_request = request.json.get("constraints")
            constraints = Utilities._convert_to_generic(
                constraints_request, Constraint
            )

            return (food_information, objective, constraints)
        except Exception as e:
            raise ValueError(f"Error processing request data: {str(e)}")

    @staticmethod
    def convert_keys_to_camel_case(response: dict) -> dict:
        return {
            Utilities._snake_to_camel(key): value
            for key, value in response.items()
        }
