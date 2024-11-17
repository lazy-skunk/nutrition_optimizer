from flask import Flask, Response, jsonify, render_template, request
from pulp import LpMaximize, LpMinimize, LpProblem, LpStatus

from src.constraint import Constraint
from src.food_information import FoodInformation
from src.nutrition_optimizer import NutritionOptimizer
from src.objective import Objective
from src.utilities import Utilities

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/optimize", methods=["POST"])
def optimize() -> Response:
    try:
        # TODO: リクエストの扱いを改善したい。
        if request is None or request.json is None:
            return jsonify({"status": "InvalidRequest", "result": {}})

        food_information_json = request.json.get("foodInformation")
        food_information_list = [
            FoodInformation(
                **{
                    Utilities.camel_to_snake(key): value
                    for key, value in item.items()
                }
            )
            for item in food_information_json
        ]

        objective_json = request.json.get("objective")[0]
        objective = Objective(
            **{
                Utilities.camel_to_snake(key): value
                for key, value in objective_json.items()
            }
        )

        constraints = request.json.get("constraints")
        constraint_list = [
            Constraint(
                **{
                    Utilities.camel_to_snake(key): value
                    for key, value in item.items()
                }
            )
            for item in constraints
        ]

        nutrition_optimizer = NutritionOptimizer(
            food_information_list, objective, constraint_list
        )
        nutrition_optimizer._initialize_lp_variables()
        nutrition_optimizer._initialize_objective_variables()
        nutrition_optimizer._initialize_lp_problem()
        nutrition_optimizer._add_constraint_to_problem()

        print("TODO: 工事中 イマココ")

        nutrition_optimizer.problem.solve()

        if LpStatus[nutrition_optimizer.problem.status] == "Optimal":
            result = {
                food: f"{nutrition_optimizer.lp_variables[food].varValue}g"
                for food in nutrition_optimizer.lp_variables
            }

            total_protein_value = sum(
                nutrition_optimizer.lp_variables[food].varValue * item.protein
                for food, item in zip(
                    nutrition_optimizer.lp_variables.keys(),
                    food_information_list,
                )
            )

            total_fat_value = sum(
                nutrition_optimizer.lp_variables[food].varValue * item.fat
                for food, item in zip(
                    nutrition_optimizer.lp_variables.keys(),
                    food_information_list,
                )
            )

            total_carbohydrate_value = sum(
                nutrition_optimizer.lp_variables[food].varValue
                * item.carbohydrates
                for food, item in zip(
                    nutrition_optimizer.lp_variables.keys(),
                    food_information_list,
                )
            )

            total_kcal_value = (
                total_protein_value * FoodInformation.PROTEIN_ENERGY_PER_GRAM
                + total_fat_value * FoodInformation.FAT_ENERGY_PER_GRAM
                + total_carbohydrate_value
                * FoodInformation.CARBOHYDRATES_ENERGY_PER_GRAM
            )

            protein_ratio = (
                total_protein_value
                * FoodInformation.PROTEIN_ENERGY_PER_GRAM
                / total_kcal_value
            ) * nutrition_optimizer._GRAM_CALCULATION_FACTOR

            fat_ratio = (
                total_fat_value
                * FoodInformation.FAT_ENERGY_PER_GRAM
                / total_kcal_value
            ) * nutrition_optimizer._GRAM_CALCULATION_FACTOR

            carbohydrate_ratio = (
                total_carbohydrate_value
                * FoodInformation.CARBOHYDRATES_ENERGY_PER_GRAM
                / total_kcal_value
            ) * nutrition_optimizer._GRAM_CALCULATION_FACTOR

            pfc_ratio = {
                "protein_ratio": f"{protein_ratio:.1f}%",
                "fat_ratio": f"{fat_ratio:.1f}%",
                "carbohydrate_ratio": f"{carbohydrate_ratio:.1f}%",
            }

            return jsonify(
                {
                    "status": "Optimal",
                    "result": result,
                    "pfc_ratio": pfc_ratio,
                }
            )
        else:
            return jsonify({"status": "Infeasible", "result": {}})

    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
