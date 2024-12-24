function addItem(templateId, targetId) {
  const template = document.getElementById(templateId).content.cloneNode(true);
  document.getElementById(targetId).appendChild(template);
}

function removeItem(button) {
  button.closest("tr").remove();
}

function updateUnitOptions(select) {
  const nutritionalComponent = select
    .closest("tr")
    .querySelector("[name='constraint-nutritional-component']");
  const unitSelect = select
    .closest("tr")
    .querySelector("[name='constraint-unit']");

  unitSelect.innerHTML = "";

  if (nutritionalComponent.value === "energy") {
    const energyTemplate = document.getElementById("unit-options-energy");
    unitSelect.appendChild(energyTemplate.content.cloneNode(true));
    unitSelect.disabled = true;
  } else {
    unitSelect.disabled = false;
    const amountRatioTemplate = document.getElementById(
      "unit-options-amount-ratio"
    );
    unitSelect.appendChild(amountRatioTemplate.content.cloneNode(true));
  }
}

function getFoodInformation() {
  return Array.from(document.querySelectorAll("#food-inputs tr")).map(
    (item) => ({
      name: item.querySelector("[name='food-name']").value,
      gramsPerUnit: parseInt(
        item.querySelector("[name='food-grams-per-unit']").value
      ),
      minimumIntake: parseInt(
        item.querySelector("[name='food-minimum-intake']").value
      ),
      maximumIntake: parseInt(
        item.querySelector("[name='food-maximum-intake']").value
      ),
      energy: parseFloat(item.querySelector("[name='food-energy']").value),
      protein: parseFloat(item.querySelector("[name='food-protein']").value),
      fat: parseFloat(item.querySelector("[name='food-fat']").value),
      carbohydrates: parseFloat(
        item.querySelector("[name='food-carbohydrates']").value
      ),
    })
  );
}

function getObjective() {
  return Array.from(document.querySelectorAll("#objective-inputs tr")).map(
    (row) => ({
      objectiveSense: row.querySelector("[name='objective-sense']").value,
      nutritionalComponent: row.querySelector(
        "[name='objective-nutritional-component']"
      ).value,
    })
  );
}

function getConstraints() {
  return Array.from(document.querySelectorAll("#constraint-inputs tr")).map(
    (row) => ({
      minMax: row.querySelector("[name='constraint-min-max']").value,
      nutritionalComponent: row.querySelector(
        "[name='constraint-nutritional-component']"
      ).value,
      unit: row.querySelector("[name='constraint-unit']").value,
      value: parseFloat(row.querySelector("[name='constraint-value']").value),
    })
  );
}

function drawPFCRatioWithTotalEnergy(pfcRatio, pfcEnergyTotalValues) {
  const nutrientComponents = ["protein", "fat", "carbohydrates"];
  const colors = [
    "rgb(255, 128, 128)",
    "rgb(128, 255, 128)",
    "rgb(128, 128, 255)",
  ];

  const data = nutrientComponents.map((nutrient, index) => {
    const capitalizedNutrient =
      nutrient.charAt(0).toUpperCase() + nutrient.slice(1);
    const grams = pfcEnergyTotalValues[nutrient];
    const ratio = parseFloat(pfcRatio[nutrient]);

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
    subtitle: {
      text: `Total Energy: ${pfcEnergyTotalValues.energy} kcal`,
    },
    series: [
      {
        name: "PFC Ratio",
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
  } else {
    clearCharts();
    alert("status: " + result.status + "\n" + "message: " + result.message);
  }
}

function clearCharts() {
  document.getElementById("food-intake-chart").textContent = "";
  document.getElementById("pfc-ratio-chart").textContent = "";
}

async function submitForm() {
  const foodInformation = getFoodInformation();
  const objective = getObjective();
  const constraints = getConstraints();

  const response = await fetch("/optimize", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      foodInformation,
      objective,
      constraints,
    }),
  });

  const result = await response.json();

  handleOptimizationResult(result);
}
