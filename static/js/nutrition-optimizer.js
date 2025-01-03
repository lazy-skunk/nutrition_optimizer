var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
import { getElementByIdOrThrow, getClosestTableRowElementOrThrow, getElementByQuerySelectorOrThrow, getElementsByQuerySelectorAllOrThrow, } from "./dom-utilities.js";
function updateUnitOptionsWithTemplate(select, templateId) {
    const template = getElementByIdOrThrow(templateId);
    const clonedTemplate = template.content.cloneNode(true);
    select.innerHTML = "";
    select.appendChild(clonedTemplate);
}
export function updateUnitOptions(select) {
    const row = getClosestTableRowElementOrThrow(select);
    const nutrientSelect = getElementByQuerySelectorOrThrow(row, "[name='constraint-nutrient']");
    const unitSelect = getElementByQuerySelectorOrThrow(row, "[name='constraint-unit']");
    if (nutrientSelect.value === "energy") {
        updateUnitOptionsWithTemplate(unitSelect, "unit-options-energy");
        unitSelect.disabled = true;
    }
    else {
        unitSelect.disabled = false;
        updateUnitOptionsWithTemplate(unitSelect, "unit-options-amount-ratio");
    }
}
function removeRowFromTable(button) {
    const row = getClosestTableRowElementOrThrow(button);
    row.remove();
}
function addEventListenersToTemplate(template) {
    const nutrientSelect = template.querySelector("[name='constraint-nutrient']");
    if (nutrientSelect) {
        nutrientSelect.addEventListener("change", () => updateUnitOptions(nutrientSelect));
    }
    const removeButton = getElementByQuerySelectorOrThrow(template, "button");
    removeButton.addEventListener("click", () => removeRowFromTable(removeButton));
}
export function appendTemplateToTable(templateId, targetId) {
    const templateElement = getElementByIdOrThrow(templateId);
    const targetElement = getElementByIdOrThrow(targetId);
    const clonedTemplate = templateElement.content.cloneNode(true);
    addEventListenersToTemplate(clonedTemplate);
    targetElement.appendChild(clonedTemplate);
}
export function initializeNutrientSelectOnChange() {
    const nutrientSelect = getElementByQuerySelectorOrThrow(document, "[name='constraint-nutrient']");
    nutrientSelect.addEventListener("change", () => {
        updateUnitOptions(nutrientSelect);
    });
}
function getFoodInformation() {
    const foodInput = getElementByIdOrThrow("food-inputs");
    const rows = getElementsByQuerySelectorAllOrThrow(foodInput, "tr");
    return Array.from(rows).map((row) => {
        const nameInput = getElementByQuerySelectorOrThrow(row, "[name='food-name']");
        const gramsPerUnitInput = getElementByQuerySelectorOrThrow(row, "[name='food-grams-per-unit']");
        const minimumIntakeInput = getElementByQuerySelectorOrThrow(row, "[name='food-minimum-intake']");
        const maximumIntakeInput = getElementByQuerySelectorOrThrow(row, "[name='food-maximum-intake']");
        const energyInput = getElementByQuerySelectorOrThrow(row, "[name='food-energy']");
        const proteinInput = getElementByQuerySelectorOrThrow(row, "[name='food-protein']");
        const fatInput = getElementByQuerySelectorOrThrow(row, "[name='food-fat']");
        const carbohydratesInput = getElementByQuerySelectorOrThrow(row, "[name='food-carbohydrates']");
        return {
            name: nameInput.value,
            gramsPerUnit: parseInt(gramsPerUnitInput.value),
            minimumIntake: parseInt(minimumIntakeInput.value),
            maximumIntake: parseInt(maximumIntakeInput.value),
            energy: parseFloat(energyInput.value),
            protein: parseFloat(proteinInput.value),
            fat: parseFloat(fatInput.value),
            carbohydrates: parseFloat(carbohydratesInput.value),
        };
    });
}
function getObjective() {
    const objectiveInput = getElementByIdOrThrow("objective-input");
    const row = getElementByQuerySelectorOrThrow(objectiveInput, "tr");
    const SenseInput = getElementByQuerySelectorOrThrow(row, "[name='objective-sense']");
    const nutrientInput = getElementByQuerySelectorOrThrow(row, "[name='objective-nutrient']");
    return {
        sense: SenseInput.value,
        nutrient: nutrientInput.value,
    };
}
function getConstraints() {
    const constraintInput = getElementByIdOrThrow("constraint-inputs");
    const rows = getElementsByQuerySelectorAllOrThrow(constraintInput, "tr");
    return Array.from(rows).map((row) => {
        const minMaxInput = getElementByQuerySelectorOrThrow(row, "[name='constraint-min-max']");
        const nutrientInput = getElementByQuerySelectorOrThrow(row, "[name='constraint-nutrient']");
        const unitInput = getElementByQuerySelectorOrThrow(row, "[name='constraint-unit']");
        const valueInput = getElementByQuerySelectorOrThrow(row, "[name='constraint-value']");
        return {
            minMax: minMaxInput.value,
            nutrient: nutrientInput.value,
            unit: unitInput.value,
            value: parseFloat(valueInput.value),
        };
    });
}
function drawPFCRatioWithTotalEnergy(pfcRatio, totalNutrientValues) {
    const nutrients = ["protein", "fat", "carbohydrates"];
    const colors = [
        "rgb(255, 128, 128)",
        "rgb(128, 255, 128)",
        "rgb(128, 128, 255)",
    ];
    const pfcData = nutrients.map((nutrient, index) => {
        const capitalizedNutrient = nutrient.charAt(0).toUpperCase() + nutrient.slice(1);
        const grams = totalNutrientValues[nutrient];
        const ratio = pfcRatio[nutrient];
        return {
            name: `${capitalizedNutrient} (${grams}g)`,
            y: ratio,
            color: colors[index],
        };
    });
    Highcharts.chart("pfc-ratio-chart", {
        chart: {
            type: "pie",
        },
        title: {
            text: "PFC Ratio",
        },
        tooltip: {
            valueSuffix: "%",
        },
        subtitle: {
            text: `Total Energy: ${totalNutrientValues.energy} kcal`,
        },
        series: [
            {
                name: "Percentage",
                colorByPoint: true,
                data: pfcData,
            },
        ],
    });
}
function drawFoodintakes(foodintakes) {
    const foodIntakesData = Object.keys(foodintakes).map((food) => ({
        name: food,
        y: foodintakes[food],
    }));
    Highcharts.chart("food-intakes-chart", {
        chart: {
            type: "bar",
        },
        title: {
            text: "Food Intakes",
        },
        xAxis: {
            categories: foodIntakesData.map((item) => item.name),
            title: {
                text: "Food Item",
            },
        },
        yAxis: {
            title: {
                text: "Units",
            },
        },
        series: [
            {
                name: "Food Intakes",
                data: foodIntakesData.map((item) => item.y),
                color: "rgb(128, 128, 255)",
                type: "bar",
            },
        ],
    });
}
function clearCharts() {
    const foodIntakesChart = getElementByIdOrThrow("food-intakes-chart");
    const pfcRatioChart = getElementByIdOrThrow("pfc-ratio-chart");
    foodIntakesChart.textContent = "";
    pfcRatioChart.textContent = "";
}
function handleOptimizationResult(result) {
    if (result.status === "Optimal") {
        drawPFCRatioWithTotalEnergy(result.pfcRatio, result.totalNutrientValues);
        drawFoodintakes(result.foodIntakes);
    }
    else {
        clearCharts();
        alert("status: " + result.status + "\n" + "message: " + result.message);
    }
}
export function optimize() {
    return __awaiter(this, void 0, void 0, function* () {
        try {
            const foodInformation = getFoodInformation();
            const objective = getObjective();
            const constraints = getConstraints();
            const response = yield fetch("/optimize", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    foodInformation,
                    objective,
                    constraints,
                }),
            });
            if (!response.ok) {
                throw new Error(`Response status: ${response.status}`);
            }
            const result = yield response.json();
            handleOptimizationResult(result);
        }
        catch (error) {
            if (error instanceof Error) {
                alert(error.message);
            }
        }
    });
}
//# sourceMappingURL=nutrition-optimizer.js.map