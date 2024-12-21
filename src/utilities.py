import re

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
    def _convert_to_food_information(data: list) -> list:
        return [
            FoodInformation(
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
    def _convert_to_constraints(data: list) -> list:
        return [
            Constraint(
                **{
                    Utilities._camel_to_snake(key): value
                    for key, value in item.items()
                }
            )
            for item in data
        ]

    @staticmethod
    def parse_request_data(request: Request) -> dict:
        try:
            if request is None or request.json is None:
                return {"status": "InvalidRequest", "result": {}}

            food_information_request_data = request.json.get("foodInformation")
            food_information = Utilities._convert_to_food_information(
                food_information_request_data
            )

            objective_request_data = request.json.get("objective")[0]
            objective = Utilities._convert_to_objective(objective_request_data)

            constraints_request_data = request.json.get("constraints")
            constraint_list = Utilities._convert_to_constraints(
                constraints_request_data
            )

            return {
                "food_information": food_information,
                "objective": objective,
                "constraints": constraint_list,
            }
        except Exception as e:
            raise ValueError(f"Error processing request data: {str(e)}")
