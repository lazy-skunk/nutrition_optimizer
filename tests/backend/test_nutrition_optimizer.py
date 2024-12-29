from src.constraint import Constraint
from src.food_information import FoodInformation
from src.nutrition_optimizer import NutritionOptimizer
from src.objective import Objective

_FOOD_INFORMATION = [
    FoodInformation(
        name="boiled_egg",
        energy=134,
        protein=12.5,
        fat=10.4,
        carbohydrates=0.3,
        grams_per_unit=50,
        minimum_intake=1,
        maximum_intake=3,
    ),
]

_OBJECTIVE = Objective(sense="maximize", nutrient="energy")

_CONSTRAINTS = [
    Constraint(
        min_max="max",
        nutrient="energy",
        unit="energy",
        value=200,
    ),
    Constraint(
        min_max="min",
        nutrient="fat",
        unit="ratio",
        value=20,
    ),
]

_INFEASIBLE_CONSTRAINTS = [
    Constraint(
        min_max="max",
        nutrient="energy",
        unit="energy",
        value=1,
    ),
]


def test_solve() -> None:
    optimizer = NutritionOptimizer(_FOOD_INFORMATION, _OBJECTIVE, _CONSTRAINTS)
    result = optimizer.solve()

    assert result["status"] == "Optimal"
    assert "food_intakes" in result
    assert "total_nutrient_values" in result
    assert "pfc_ratio" in result

    assert result["food_intakes"]["boiled_egg"] == 2
    assert result["total_nutrient_values"]["energy"] == 134


def test_infeasible() -> None:
    optimizer = NutritionOptimizer(
        _FOOD_INFORMATION, _OBJECTIVE, _INFEASIBLE_CONSTRAINTS
    )
    result = optimizer.solve()

    assert result["status"] == "Infeasible"
    assert "message" in result
    assert (
        result["message"] == "Please review the constraints,"
        " the grams per unit, or the intake values."
    )
