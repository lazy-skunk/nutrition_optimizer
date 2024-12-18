import re

from flask import Request

from src.constraint import Constraint
from src.food_information import FoodInformation
from src.objective import Objective


class Utilities:
    @staticmethod
    def _camel_to_snake(camel_case_str: str) -> str:
        return re.sub(r"([a-z])([A-Z])", r"\1_\2", camel_case_str).lower()

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
            food_information_list = Utilities._convert_to_food_information(
                food_information_request_data
            )

            objective_request_data = request.json.get("objective")[0]
            objective = Utilities._convert_to_objective(objective_request_data)

            constraints_request_data = request.json.get("constraints")
            constraint_list = Utilities._convert_to_constraints(
                constraints_request_data
            )

            return {
                "food_information_list": food_information_list,
                "objective": objective,
                "constraints": constraint_list,
            }
        except Exception as e:
            raise ValueError(f"Error processing request data: {str(e)}")
