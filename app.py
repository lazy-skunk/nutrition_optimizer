from flask import Flask, Response, jsonify, render_template, request

from src.nutrition_optimizer import NutritionOptimizer
from src.utilities import Utilities

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/optimize", methods=["POST"])
def optimize() -> Response:
    try:
        parsed_data = Utilities.parse_request_data(request)

        food_information = parsed_data["food_information"]
        objective = parsed_data["objective"]
        constraints = parsed_data["constraints"]

        nutrition_optimizer = NutritionOptimizer(
            food_information, objective, constraints
        )
        result = nutrition_optimizer.solve()

        return jsonify(result)
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
