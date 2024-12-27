"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
function addItem(templateId, targetId) {
    const templateElement = document.getElementById(templateId);
    const targetElement = document.getElementById(targetId);
    if (!templateElement) {
        throw new Error(`Template element with ID "${templateId}" not found.`);
    }
    if (!targetElement) {
        throw new Error(`Target element with ID "${targetId}" not found.`);
    }
    const template = templateElement.content.cloneNode(true);
    targetElement.appendChild(template);
}
function removeItem(button) {
    const row = button.closest("tr");
    if (!row) {
        throw new Error("Row element not found.");
    }
    row.remove();
}
function updateUnitOptions(select) {
    const row = select.closest("tr");
    if (!row) {
        throw new Error("Row element not found.");
    }
    const nutritionalComponentSelect = row.querySelector("[name='constraint-nutritional-component']");
    const unitSelect = row.querySelector("[name='constraint-unit']");
    if (!nutritionalComponentSelect) {
        throw new Error("Nutritional component select element not found in row.");
    }
    if (!unitSelect) {
        throw new Error("Unit select element not found in row.");
    }
    unitSelect.innerHTML = "";
    if (nutritionalComponentSelect.textContent === "energy") {
        const energyTemplate = document.getElementById("unit-options-energy");
        if (!energyTemplate) {
            throw new Error("energyTemplate with ID 'unit-options-energy' not found.");
        }
        unitSelect.appendChild(energyTemplate.content.cloneNode(true));
        unitSelect.disabled = true;
    }
    else {
        unitSelect.disabled = false;
        const amountRatioTemplate = document.getElementById("unit-options-amount-ratio");
        if (!amountRatioTemplate) {
            throw new Error("amountRatioTemplate with ID 'unit-options-amount-ratio' not found.");
        }
        unitSelect.appendChild(amountRatioTemplate.content.cloneNode(true));
    }
}
function getFoodInformation() {
    return Array.from(document.querySelectorAll("#food-inputs tr")).map((row) => {
        const nameElement = row.querySelector("[name='food-name']");
        const gramsPerUnitElement = row.querySelector("[name='food-grams-per-unit']");
        const minimumIntakeElement = row.querySelector("[name='food-minimum-intake']");
        const maximumIntakeElement = row.querySelector("[name='food-maximum-intake']");
        const energyElement = row.querySelector("[name='food-energy']");
        const proteinElement = row.querySelector("[name='food-protein']");
        const fatElement = row.querySelector("[name='food-fat']");
        const carbohydratesElement = row.querySelector("[name='food-carbohydrates']");
        return {
            name: nameElement.value,
            gramsPerUnit: parseInt(gramsPerUnitElement.value),
            minimumIntake: parseInt(minimumIntakeElement.value),
            maximumIntake: parseInt(maximumIntakeElement.value),
            energy: parseFloat(energyElement.value),
            protein: parseFloat(proteinElement.value),
            fat: parseFloat(fatElement.value),
            carbohydrates: parseFloat(carbohydratesElement.value),
        };
    });
}
function getObjective() {
    return Array.from(document.querySelectorAll("#objective-inputs tr")).map((row) => {
        const objectiveSenseElement = row.querySelector("[name='objective-sense']");
        const nutritionalComponentElement = row.querySelector("[name='objective-nutritional-component']");
        return {
            objectiveSense: objectiveSenseElement.value,
            nutritionalComponent: nutritionalComponentElement.value,
        };
    });
}
function getConstraints() {
    return Array.from(document.querySelectorAll("#constraint-inputs tr")).map((row) => {
        const minMaxElement = row.querySelector("[name='constraint-min-max']");
        const nutritionalComponentElement = row.querySelector("[name='constraint-nutritional-component']");
        const unitElement = row.querySelector("[name='constraint-unit']");
        const valueElement = row.querySelector("[name='constraint-value']");
        return {
            minMax: minMaxElement.value,
            nutritionalComponent: nutritionalComponentElement.value,
            unit: unitElement.value,
            value: parseFloat(valueElement.value),
        };
    });
}
function drawPFCRatioWithTotalEnergy(pfcRatio, pfcEnergyTotalValues) {
    const nutrientComponents = ["protein", "fat", "carbohydrates"];
    const colors = [
        "rgb(255, 128, 128)",
        "rgb(128, 255, 128)",
        "rgb(128, 128, 255)",
    ];
    const data = nutrientComponents.map((nutrient, index) => {
        const capitalizedNutrient = nutrient.charAt(0).toUpperCase() + nutrient.slice(1);
        const grams = pfcEnergyTotalValues[nutrient];
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
            text: `Total Energy: ${pfcEnergyTotalValues.energy} kcal`,
        },
        series: [
            {
                name: "Percentage",
                colorByPoint: true,
                data: data,
            },
        ],
    });
}
function drawFoodIntake(foodIntake) {
    const data = Object.keys(foodIntake).map((food) => ({
        name: food,
        y: foodIntake[food],
    }));
    Highcharts.chart("food-intake-chart", {
        chart: {
            type: "bar",
        },
        title: {
            text: "Food Intake",
        },
        xAxis: {
            categories: data.map((item) => item.name),
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
                name: "Food Intake",
                data: data.map((item) => item.y),
                color: "rgb(128, 128, 255)",
            },
        ],
    });
}
function handleOptimizationResult(result) {
    if (result.status === "Optimal") {
        drawPFCRatioWithTotalEnergy(result.pfcRatio, result.pfcEnergyTotalValues);
        drawFoodIntake(result.foodIntake);
    }
    else {
        clearCharts();
        alert("status: " + result.status + "\n" + "message: " + result.message);
    }
}
function clearCharts() {
    const foodIntakeChart = document.getElementById("food-intake-chart");
    const pfcRatioChart = document.getElementById("pfc-ratio-chart");
    if (!foodIntakeChart) {
        throw new Error("Food intake chart not found.");
    }
    if (!pfcRatioChart) {
        throw new Error("PFC ratio chart not found.");
    }
    foodIntakeChart.textContent = "";
    pfcRatioChart.textContent = "";
}
function submitForm() {
    return __awaiter(this, void 0, void 0, function* () {
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
        const result = yield response.json();
        handleOptimizationResult(result);
    });
}
//# sourceMappingURL=script.js.map