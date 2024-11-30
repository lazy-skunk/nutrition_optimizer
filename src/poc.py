from pulp import LpMaximize, LpProblem, LpStatus, LpVariable

FOODS = {
    "rice": {"protein": 2.8, "fat": 1, "carbohydrate": 35.6, "kcal": 152},
    "chicken_fillet": {
        "protein": 29.6,
        "fat": 1,
        "carbohydrate": 0,
        "kcal": 121,
    },
    "boiled_egg": {
        "protein": 12.5,
        "fat": 10.4,
        "carbohydrate": 0.3,
        "kcal": 134,
    },
    "broccoli": {"protein": 3.9, "fat": 0.4, "carbohydrate": 5.2, "kcal": 30},
    "xplosion": {
        "protein": 70.1,
        "fat": 6.4,
        "carbohydrate": 14.6,
        "kcal": 386,
    },
}


# rice_grams = LpVariable("米の量", lowBound=200, upBound=800, cat="Integer")
# chicken_fillet_units = LpVariable(
#     "ささみの数", lowBound=150, upBound=300, cat="Integer"
# )
# boiled_egg_units = LpVariable(
#     "ゆで卵の数", lowBound=150, upBound=200, cat="Integer"
# )
# broccoli_units = LpVariable(
#     "ブロッコリーの数", lowBound=45, upBound=90, cat="Integer"
# )
# xplosion_units = LpVariable(
#     "プロテインの数", lowBound=90, upBound=120, cat="Integer"
# )

# CHICKEN_FILLET_GRAMS_PER_UNIT = 1
# BOILED_EGG_GRAMS_PER_UNIT = 1
# BROCCOLI_GRAMS_PER_UNIT = 1
# XPLOSION_GRAMS_PER_UNIT = 1

rice_grams = LpVariable("米の量", lowBound=200, upBound=800, cat="Integer")
chicken_fillet_units = LpVariable(
    "ささみの数", lowBound=6, upBound=8, cat="Integer"
)
boiled_egg_units = LpVariable(
    "ゆで卵の数", lowBound=3, upBound=4, cat="Integer"
)
broccoli_units = LpVariable(
    "ブロッコリーの数", lowBound=6, upBound=9, cat="Integer"
)
xplosion_units = LpVariable(
    "プロテインの数", lowBound=2, upBound=3, cat="Integer"
)

CHICKEN_FILLET_GRAMS_PER_UNIT = 40
BOILED_EGG_GRAMS_PER_UNIT = 50
BROCCOLI_GRAMS_PER_UNIT = 15
XPLOSION_GRAMS_PER_UNIT = 30

GRAM_CALCULATION_FACTOR = 100

total_kcal = (
    FOODS["rice"]["kcal"] * rice_grams / GRAM_CALCULATION_FACTOR
    + FOODS["chicken_fillet"]["kcal"]
    * CHICKEN_FILLET_GRAMS_PER_UNIT
    * chicken_fillet_units
    / GRAM_CALCULATION_FACTOR
    + FOODS["boiled_egg"]["kcal"]
    * BOILED_EGG_GRAMS_PER_UNIT
    * boiled_egg_units
    / GRAM_CALCULATION_FACTOR
    + FOODS["broccoli"]["kcal"]
    * BROCCOLI_GRAMS_PER_UNIT
    * broccoli_units
    / GRAM_CALCULATION_FACTOR
    + FOODS["xplosion"]["kcal"]
    * XPLOSION_GRAMS_PER_UNIT
    * xplosion_units
    / GRAM_CALCULATION_FACTOR
)

total_protein_grams = (
    FOODS["rice"]["protein"] * rice_grams / GRAM_CALCULATION_FACTOR
    + FOODS["chicken_fillet"]["protein"]
    * CHICKEN_FILLET_GRAMS_PER_UNIT
    * chicken_fillet_units
    / GRAM_CALCULATION_FACTOR
    + FOODS["boiled_egg"]["protein"]
    * BOILED_EGG_GRAMS_PER_UNIT
    * boiled_egg_units
    / GRAM_CALCULATION_FACTOR
    + FOODS["broccoli"]["protein"]
    * BROCCOLI_GRAMS_PER_UNIT
    * broccoli_units
    / GRAM_CALCULATION_FACTOR
    + FOODS["xplosion"]["protein"]
    * XPLOSION_GRAMS_PER_UNIT
    * xplosion_units
    / GRAM_CALCULATION_FACTOR
)

total_fat_grams = (
    FOODS["rice"]["fat"] * rice_grams / GRAM_CALCULATION_FACTOR
    + FOODS["chicken_fillet"]["fat"]
    * CHICKEN_FILLET_GRAMS_PER_UNIT
    * chicken_fillet_units
    / GRAM_CALCULATION_FACTOR
    + FOODS["boiled_egg"]["fat"]
    * BOILED_EGG_GRAMS_PER_UNIT
    * boiled_egg_units
    / GRAM_CALCULATION_FACTOR
    + FOODS["broccoli"]["fat"]
    * BROCCOLI_GRAMS_PER_UNIT
    * broccoli_units
    / GRAM_CALCULATION_FACTOR
    + FOODS["xplosion"]["fat"]
    * XPLOSION_GRAMS_PER_UNIT
    * xplosion_units
    / GRAM_CALCULATION_FACTOR
)

problem = LpProblem("制約に基づきカロリーを最大化", sense=LpMaximize)
problem += total_kcal, "カロリーを最大化"
problem += total_kcal <= 1700, "カロリーの上限"
problem += total_protein_grams <= 160, "たんぱく質のグラム数上限"
problem += total_protein_grams >= 150, "たんぱく質のグラム数下限"
problem += total_fat_grams * 9 <= total_kcal * 0.2, "脂質の割合上限"

problem.solve()

if LpStatus[problem.status] == "Optimal":
    print("最適解が見つかりました。")

    print("###")
    print("1 日の総摂取量は次のとおりです。")
    print(f"ご飯: {rice_grams.varValue} g")
    print(f"ブロッコリー: {broccoli_units.varValue} g")
    print(f"ささみ: {chicken_fillet_units.varValue} g")
    print(f"ゆで卵: {boiled_egg_units.varValue} g")
    print(f"プロテイン: {xplosion_units.varValue} g")

    total_protein_value = (
        FOODS["rice"]["protein"]
        * rice_grams.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["broccoli"]["protein"]
        * BROCCOLI_GRAMS_PER_UNIT
        * broccoli_units.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["chicken_fillet"]["protein"]
        * CHICKEN_FILLET_GRAMS_PER_UNIT
        * chicken_fillet_units.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["boiled_egg"]["protein"]
        * BOILED_EGG_GRAMS_PER_UNIT
        * boiled_egg_units.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["xplosion"]["protein"]
        * XPLOSION_GRAMS_PER_UNIT
        * xplosion_units.varValue
        / GRAM_CALCULATION_FACTOR
    )
    total_fat_value = (
        FOODS["rice"]["fat"] * rice_grams.varValue / GRAM_CALCULATION_FACTOR
        + FOODS["broccoli"]["fat"]
        * BROCCOLI_GRAMS_PER_UNIT
        * broccoli_units.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["chicken_fillet"]["fat"]
        * CHICKEN_FILLET_GRAMS_PER_UNIT
        * chicken_fillet_units.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["boiled_egg"]["fat"]
        * BOILED_EGG_GRAMS_PER_UNIT
        * boiled_egg_units.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["xplosion"]["fat"]
        * XPLOSION_GRAMS_PER_UNIT
        * xplosion_units.varValue
        / GRAM_CALCULATION_FACTOR
    )
    total_carbohydrate_value = (
        FOODS["rice"]["carbohydrate"]
        * rice_grams.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["broccoli"]["carbohydrate"]
        * BROCCOLI_GRAMS_PER_UNIT
        * broccoli_units.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["chicken_fillet"]["carbohydrate"]
        * CHICKEN_FILLET_GRAMS_PER_UNIT
        * chicken_fillet_units.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["boiled_egg"]["carbohydrate"]
        * BOILED_EGG_GRAMS_PER_UNIT
        * boiled_egg_units.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["xplosion"]["carbohydrate"]
        * XPLOSION_GRAMS_PER_UNIT
        * xplosion_units.varValue
        / GRAM_CALCULATION_FACTOR
    )
    total_kcal_value = (
        FOODS["rice"]["kcal"] * rice_grams.varValue / GRAM_CALCULATION_FACTOR
        + FOODS["broccoli"]["kcal"]
        * BROCCOLI_GRAMS_PER_UNIT
        * broccoli_units.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["chicken_fillet"]["kcal"]
        * CHICKEN_FILLET_GRAMS_PER_UNIT
        * chicken_fillet_units.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["boiled_egg"]["kcal"]
        * BOILED_EGG_GRAMS_PER_UNIT
        * boiled_egg_units.varValue
        / GRAM_CALCULATION_FACTOR
        + FOODS["xplosion"]["kcal"]
        * XPLOSION_GRAMS_PER_UNIT
        * xplosion_units.varValue
        / GRAM_CALCULATION_FACTOR
    )

    print("###")
    print(f"総たんぱく質: {total_protein_value:.1f} g")
    print(f"総脂質: {total_fat_value:.1f} g")
    print(f"総炭水化物: {total_carbohydrate_value:.1f} g")
    print(f"総カロリー: {total_kcal_value:.1f} kcal")

    print("###")
    PROTEIN_KCAL_PER_GRAM = 4
    print(
        f"たんぱく質割合: {GRAM_CALCULATION_FACTOR * (total_protein_value * PROTEIN_KCAL_PER_GRAM) / total_kcal_value:.1f}%"
    )
    FAT_KCAL_PER_GRAM = 9
    print(
        f"脂質割合: {GRAM_CALCULATION_FACTOR * (total_fat_value * FAT_KCAL_PER_GRAM) / total_kcal_value:.1f}%"
    )
    CARBOHYDRATE_KCAL_PER_GRAM = 4
    print(
        f"炭水化物割合: {GRAM_CALCULATION_FACTOR * (total_carbohydrate_value * CARBOHYDRATE_KCAL_PER_GRAM) / total_kcal_value:.1f}%"
    )
else:
    print(
        "最適解が見つかりませんでした。制約条件を見直すことで最適解が見つかる場合があります。"
    )
