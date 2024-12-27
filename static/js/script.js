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
    const rows = document.querySelectorAll("#food-inputs tr");
    return Array.from(rows).map((row) => {
        const nameInput = row.querySelector("[name='food-name']");
        const gramsPerUnitInput = row.querySelector("[name='food-grams-per-unit']");
        const minimumIntakeInput = row.querySelector("[name='food-minimum-intake']");
        const maximumIntakeInput = row.querySelector("[name='food-maximum-intake']");
        const energyInput = row.querySelector("[name='food-energy']");
        const proteinInput = row.querySelector("[name='food-protein']");
        const fatInput = row.querySelector("[name='food-fat']");
        const carbohydratesInput = row.querySelector("[name='food-carbohydrates']");
        if (!nameInput ||
            !gramsPerUnitInput ||
            !minimumIntakeInput ||
            !maximumIntakeInput ||
            !energyInput ||
            !proteinInput ||
            !fatInput ||
            !carbohydratesInput) {
            throw new Error("One or more required input elements not found in the row.");
        }
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
    const row = document.querySelector("#objective-inputs tr");
    if (!row) {
        throw new Error("Row element not found.");
    }
    const objectiveSenseInput = row.querySelector("[name='objective-sense']");
    const nutritionalComponentInput = row.querySelector("[name='objective-nutritional-component']");
    if (!objectiveSenseInput || !nutritionalComponentInput) {
        throw new Error("Required input elements not found in the row.");
    }
    return {
        objectiveSense: objectiveSenseInput.value,
        nutritionalComponent: nutritionalComponentInput.value,
    };
}
function getConstraints() {
    const rows = document.querySelectorAll("#constraint-inputs tr");
    return Array.from(rows).map((row) => {
        const minMaxInput = row.querySelector("[name='constraint-min-max']");
        const nutritionalComponentInput = row.querySelector("[name='constraint-nutritional-component']");
        const unitInput = row.querySelector("[name='constraint-unit']");
        const valueInput = row.querySelector("[name='constraint-value']");
        if (!minMaxInput ||
            !nutritionalComponentInput ||
            !unitInput ||
            !valueInput) {
            throw new Error("Required input elements not found in the row.");
        }
        return {
            minMax: minMaxInput.value,
            nutritionalComponent: nutritionalComponentInput.value,
            unit: unitInput.value,
            value: parseFloat(valueInput.value),
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
    const pfcData = nutrientComponents.map((nutrient, index) => {
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
                data: pfcData,
            },
        ],
    });
}
function drawFoodIntake(foodIntake) {
    const foodIntakeData = Object.keys(foodIntake).map((food) => ({
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
            categories: foodIntakeData.map((item) => item.name),
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
                data: foodIntakeData.map((item) => item.y),
                color: "rgb(128, 128, 255)",
            },
        ],
    });
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