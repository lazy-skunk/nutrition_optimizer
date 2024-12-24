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
        food_information, objective, constraints = (
            Utilities.parse_request_data(request)
        )

        nutrition_optimizer = NutritionOptimizer(
            food_information, objective, constraints
        )
        result = nutrition_optimizer.solve()

        parsed_result = Utilities.convert_keys_to_camel_case(result)
        return jsonify(parsed_result)
    except Exception as e:
        return jsonify({"status": "Error", "message": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
