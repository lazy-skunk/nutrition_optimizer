from flask import Flask, Response, jsonify, render_template, request
from pulp import LpMaximize, LpMinimize, LpProblem, LpStatus, LpVariable

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

        # TODO: lp_variables を消してもいいかの判断をしてもいいかな。
        print("breakpoint 用")

        if objective_json["problem"] == "minimize":
            problem = LpProblem(
                f"minimize_{objective_json['nutritionalComponent']}",
                LpMinimize,
            )
        else:
            problem = LpProblem(
                f"maximize_{objective_json['nutritionalComponent']}",
                LpMaximize,
            )

        problem += nutrition_optimizer.total_energy, "Maximize_Energy"

        for constraint in constraints:
            if (
                constraint["nutritionalComponent"] == "energy"
                and constraint["minMax"] == "max"
            ):
                problem += (
                    nutrition_optimizer.total_energy <= constraint["value"],
                    "Max_Energy",
                )
                continue

            if (
                constraint["nutritionalComponent"] == "protein"
                and constraint["minMax"] == "max"
            ):
                problem += (
                    nutrition_optimizer.total_protein <= constraint["value"],
                    "Max_Protein",
                )
                continue

            if (
                constraint["nutritionalComponent"] == "protein"
                and constraint["minMax"] == "min"
            ):
                problem += (
                    nutrition_optimizer.total_protein >= constraint["value"],
                    "Min_Protein",
                )
                continue

            if (
                constraint["nutritionalComponent"] == "fat"
                and constraint["minMax"] == "max"
            ):
                total_fat_energy = nutrition_optimizer.total_fat * 9
                problem += (
                    total_fat_energy
                    <= nutrition_optimizer.total_energy
                    * (constraint["value"] / 100),
                    "Max_Fat",
                )
                continue

        problem.solve()

        if LpStatus[problem.status] == "Optimal":
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
