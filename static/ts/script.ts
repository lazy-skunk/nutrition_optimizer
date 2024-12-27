function addItem(templateId: string, targetId: string): void {
  const templateElement = document.getElementById(
    templateId
  ) as HTMLTemplateElement | null;
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

function removeItem(button: HTMLButtonElement): void {
  const row = button.closest("tr");

  if (!row) {
    throw new Error("Row element not found.");
  }

  row.remove();
}

function updateUnitOptions(select: HTMLSelectElement) {
  const row = select.closest("tr");
  if (!row) {
    throw new Error("Row element not found.");
  }

  const nutritionalComponentSelect = row.querySelector(
    "[name='constraint-nutritional-component']"
  ) as HTMLSelectElement;
  const unitSelect = row.querySelector(
    "[name='constraint-unit']"
  ) as HTMLSelectElement;
  if (!nutritionalComponentSelect) {
    throw new Error("Nutritional component select element not found in row.");
  }
  if (!unitSelect) {
    throw new Error("Unit select element not found in row.");
  }

  unitSelect.innerHTML = "";

  if (nutritionalComponentSelect.textContent === "energy") {
    const energyTemplate = document.getElementById(
      "unit-options-energy"
    ) as HTMLTemplateElement;

    if (!energyTemplate) {
      throw new Error(
        "energyTemplate with ID 'unit-options-energy' not found."
      );
    }

    unitSelect.appendChild(energyTemplate.content.cloneNode(true));
    unitSelect.disabled = true;
  } else {
    unitSelect.disabled = false;
    const amountRatioTemplate = document.getElementById(
      "unit-options-amount-ratio"
    ) as HTMLTemplateElement;

    if (!amountRatioTemplate) {
      throw new Error(
        "amountRatioTemplate with ID 'unit-options-amount-ratio' not found."
      );
    }

    unitSelect.appendChild(amountRatioTemplate.content.cloneNode(true));
  }
}

interface FoodInformation {
  name: string;
  gramsPerUnit: number;
  minimumIntake: number;
  maximumIntake: number;
  energy: number;
  protein: number;
  fat: number;
  carbohydrates: number;
}

function getFoodInformation(): FoodInformation[] {
  return Array.from(document.querySelectorAll("#food-inputs tr")).map((row) => {
    const nameElement = row.querySelector(
      "[name='food-name']"
    ) as HTMLInputElement;
    const gramsPerUnitElement = row.querySelector(
      "[name='food-grams-per-unit']"
    ) as HTMLInputElement;
    const minimumIntakeElement = row.querySelector(
      "[name='food-minimum-intake']"
    ) as HTMLInputElement;
    const maximumIntakeElement = row.querySelector(
      "[name='food-maximum-intake']"
    ) as HTMLInputElement;
    const energyElement = row.querySelector(
      "[name='food-energy']"
    ) as HTMLInputElement;
    const proteinElement = row.querySelector(
      "[name='food-protein']"
    ) as HTMLInputElement;
    const fatElement = row.querySelector(
      "[name='food-fat']"
    ) as HTMLInputElement;
    const carbohydratesElement = row.querySelector(
      "[name='food-carbohydrates']"
    ) as HTMLInputElement;

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

interface Objective {
  objectiveSense: string;
  nutritionalComponent: string;
}

function getObjective(): Objective[] {
  return Array.from(document.querySelectorAll("#objective-inputs tr")).map(
    (row) => {
      const objectiveSenseElement = row.querySelector(
        "[name='objective-sense']"
      ) as HTMLInputElement;
      const nutritionalComponentElement = row.querySelector(
        "[name='objective-nutritional-component']"
      ) as HTMLInputElement;

      return {
        objectiveSense: objectiveSenseElement.value,
        nutritionalComponent: nutritionalComponentElement.value,
      };
    }
  );
}

interface Constraint {
  minMax: string;
  nutritionalComponent: string;
  unit: string;
  value: number;
}

function getConstraints(): Constraint[] {
  return Array.from(document.querySelectorAll("#constraint-inputs tr")).map(
    (row) => {
      const minMaxElement = row.querySelector(
        "[name='constraint-min-max']"
      ) as HTMLInputElement;
      const nutritionalComponentElement = row.querySelector(
        "[name='constraint-nutritional-component']"
      ) as HTMLInputElement;
      const unitElement = row.querySelector(
        "[name='constraint-unit']"
      ) as HTMLInputElement;
      const valueElement = row.querySelector(
        "[name='constraint-value']"
      ) as HTMLInputElement;

      return {
        minMax: minMaxElement.value,
        nutritionalComponent: nutritionalComponentElement.value,
        unit: unitElement.value,
        value: parseFloat(valueElement.value),
      };
    }
  );
}

interface PFCRatio {
  [key: string]: number;
}

interface PFCEnergyTotalValues {
  [key: string]: number;
}

interface PFCData {
  name: string;
  y: number;
  color: string;
}

function drawPFCRatioWithTotalEnergy(
  pfcRatio: PFCRatio,
  pfcEnergyTotalValues: PFCEnergyTotalValues
): void {
  const nutrientComponents: string[] = ["protein", "fat", "carbohydrates"];
  const colors: string[] = [
    "rgb(255, 128, 128)",
    "rgb(128, 255, 128)",
    "rgb(128, 128, 255)",
  ];

  const data: PFCData[] = nutrientComponents.map((nutrient, index) => {
    const capitalizedNutrient =
      nutrient.charAt(0).toUpperCase() + nutrient.slice(1);
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
    ] as unknown as Highcharts.SeriesOptions[],
  } as Highcharts.Options);
}

interface FoodIntake {
  [key: string]: number;
}

function drawFoodIntake(foodIntake: FoodIntake): void {
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

interface Result {
  status: string;
  pfcRatio: PFCRatio;
  pfcEnergyTotalValues: PFCEnergyTotalValues;
  foodIntake: FoodIntake;
  message: string;
}

function handleOptimizationResult(result: Result): void {
  if (result.status === "Optimal") {
    drawPFCRatioWithTotalEnergy(result.pfcRatio, result.pfcEnergyTotalValues);
    drawFoodIntake(result.foodIntake);
  } else {
    clearCharts();
    alert("status: " + result.status + "\n" + "message: " + result.message);
  }
}

function clearCharts(): void {
  const foodIntakeChart = document.getElementById(
    "food-intake-chart"
  ) as HTMLElement | null;
  const pfcRatioChart = document.getElementById(
    "pfc-ratio-chart"
  ) as HTMLElement | null;

  if (!foodIntakeChart) {
    throw new Error("Food intake chart not found.");
  }
  if (!pfcRatioChart) {
    throw new Error("PFC ratio chart not found.");
  }

  foodIntakeChart.textContent = "";
  pfcRatioChart.textContent = "";
}

async function submitForm(): Promise<void> {
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
