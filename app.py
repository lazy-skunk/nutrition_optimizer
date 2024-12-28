from flask import Flask, Response, jsonify, render_template, request
from flask.cli import load_dotenv

from src.nutrition_optimizer import NutritionOptimizer
from src.singleton_logger import SingletonLogger
from src.utilities import Utilities


def create_app() -> Flask:
    load_dotenv()
    SingletonLogger.initialize()

    app = Flask(__name__)
    return app


app = create_app()


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/optimize", methods=["POST"])
def optimize() -> Response:
    try:
        logger = SingletonLogger.get_logger()
        food_information, objective, constraints = (
            Utilities.parse_request_data(request)
        )

        nutrition_optimizer = NutritionOptimizer(
            food_information, objective, constraints
        )
        result = nutrition_optimizer.solve()

        parsed_result = Utilities.convert_keys_to_camel_case(result)
        return jsonify(parsed_result)
    except ValueError as e:
        logger.warning(f"Invalid request data: {str(e)}")
        return jsonify({"status": "Error", "message": "Invalid request data"})
    except Exception as e:
        logger.warning(f"Error during optimization: {str(e)}")
        return jsonify({"status": "Error", "message": str(e)})


if __name__ == "__main__":
    app.run(debug=True)
