import {
  getElementByIdOrThrow,
  getClosestTableRowElementOrThrow,
  getElementByQuerySelectorOrThrow,
  getElementsByQuerySelectorAllOrThrow,
} from "./dom-utilities";

function updateUnitOptionsWithTemplate(
  select: HTMLSelectElement,
  templateId: string
): void {
  const template = getElementByIdOrThrow<HTMLTemplateElement>(templateId);
  const clonedTemplate = template.content.cloneNode(true);

  select.innerHTML = "";
  select.appendChild(clonedTemplate);
}

export function updateUnitOptions(select: HTMLSelectElement) {
  const row = getClosestTableRowElementOrThrow(select);

  const nutrientSelect = getElementByQuerySelectorOrThrow<HTMLSelectElement>(
    row,
    "[name='constraint-nutrient']"
  );
  const unitSelect = getElementByQuerySelectorOrThrow<HTMLSelectElement>(
    row,
    "[name='constraint-unit']"
  );

  if (nutrientSelect.value === "energy") {
    updateUnitOptionsWithTemplate(unitSelect, "unit-options-energy");
    unitSelect.disabled = true;
  } else {
    unitSelect.disabled = false;
    updateUnitOptionsWithTemplate(unitSelect, "unit-options-amount-ratio");
  }
}

function removeRowFromTable(button: HTMLButtonElement): void {
  const row = getClosestTableRowElementOrThrow(button);

  row.remove();
}

function addEventListenersToTemplate(template: HTMLTemplateElement): void {
  const nutrientSelect = template.querySelector(
    "[name='constraint-nutrient']"
  ) as HTMLSelectElement;
  if (nutrientSelect) {
    nutrientSelect.addEventListener("change", () =>
      updateUnitOptions(nutrientSelect)
    );
  }

  const removeButton = getElementByQuerySelectorOrThrow<HTMLButtonElement>(
    template,
    "button"
  );
  removeButton.addEventListener("click", () =>
    removeRowFromTable(removeButton)
  );
}

export function appendTemplateToTable(
  templateId: string,
  targetId: string
): void {
  const templateElement =
    getElementByIdOrThrow<HTMLTemplateElement>(templateId);
  const targetElement = getElementByIdOrThrow<HTMLTemplateElement>(targetId);

  const clonedTemplate = templateElement.content.cloneNode(
    true
  ) as HTMLTemplateElement;
  addEventListenersToTemplate(clonedTemplate);

  targetElement.appendChild(clonedTemplate);
}

export function initializeNutrientSelectOnChange(): void {
  const nutrientSelect = getElementByQuerySelectorOrThrow<HTMLSelectElement>(
    document,
    "[name='constraint-nutrient']"
  );

  nutrientSelect.addEventListener("change", () => {
    updateUnitOptions(nutrientSelect);
  });
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
  const foodInput = getElementByIdOrThrow<HTMLTableElement>("food-inputs");
  const rows = getElementsByQuerySelectorAllOrThrow(foodInput, "tr");

  return Array.from(rows).map((row) => {
    const nameInput = getElementByQuerySelectorOrThrow<HTMLInputElement>(
      row,
      "[name='food-name']"
    );
    const gramsPerUnitInput =
      getElementByQuerySelectorOrThrow<HTMLInputElement>(
        row,
        "[name='food-grams-per-unit']"
      );
    const minimumIntakeInput =
      getElementByQuerySelectorOrThrow<HTMLInputElement>(
        row,
        "[name='food-minimum-intake']"
      );
    const maximumIntakeInput =
      getElementByQuerySelectorOrThrow<HTMLInputElement>(
        row,
        "[name='food-maximum-intake']"
      );
    const energyInput = getElementByQuerySelectorOrThrow<HTMLInputElement>(
      row,
      "[name='food-energy']"
    );
    const proteinInput = getElementByQuerySelectorOrThrow<HTMLInputElement>(
      row,
      "[name='food-protein']"
    );
    const fatInput = getElementByQuerySelectorOrThrow<HTMLInputElement>(
      row,
      "[name='food-fat']"
    );
    const carbohydratesInput =
      getElementByQuerySelectorOrThrow<HTMLInputElement>(
        row,
        "[name='food-carbohydrates']"
      );

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

interface Objective {
  sense: string;
  nutrient: string;
}

function getObjective(): Objective {
  const objectiveInput =
    getElementByIdOrThrow<HTMLTableElement>("objective-input");
  const row = getElementByQuerySelectorOrThrow<HTMLTableRowElement>(
    objectiveInput,
    "tr"
  );

  const SenseInput = getElementByQuerySelectorOrThrow<HTMLInputElement>(
    row,
    "[name='objective-sense']"
  );
  const nutrientInput = getElementByQuerySelectorOrThrow<HTMLInputElement>(
    row,
    "[name='objective-nutrient']"
  );

  return {
    sense: SenseInput.value,
    nutrient: nutrientInput.value,
  };
}

interface Constraint {
  minMax: string;
  nutrient: string;
  unit: string;
  value: number;
}

function getConstraints(): Constraint[] {
  const constraintInput =
    getElementByIdOrThrow<HTMLTableElement>("constraint-inputs");
  const rows = getElementsByQuerySelectorAllOrThrow(constraintInput, "tr");

  return Array.from(rows).map((row) => {
    const minMaxInput = getElementByQuerySelectorOrThrow<HTMLInputElement>(
      row,
      "[name='constraint-min-max']"
    );
    const nutrientInput = getElementByQuerySelectorOrThrow<HTMLInputElement>(
      row,
      "[name='constraint-nutrient']"
    );
    const unitInput = getElementByQuerySelectorOrThrow<HTMLInputElement>(
      row,
      "[name='constraint-unit']"
    );
    const valueInput = getElementByQuerySelectorOrThrow<HTMLInputElement>(
      row,
      "[name='constraint-value']"
    );

    return {
      minMax: minMaxInput.value,
      nutrient: nutrientInput.value,
      unit: unitInput.value,
      value: parseFloat(valueInput.value),
    };
  });
}

interface PFCRatio {
  [key: string]: number;
}

interface TotalNutrientValues {
  [key: string]: number;
}

interface PFCData {
  name: string;
  y: number;
  color: string;
}

function drawPFCRatioWithTotalEnergy(
  pfcRatio: PFCRatio,
  totalNutrientValues: TotalNutrientValues
): void {
  const nutrients: string[] = ["protein", "fat", "carbohydrates"];
  const colors: string[] = [
    "rgb(255, 128, 128)",
    "rgb(128, 255, 128)",
    "rgb(128, 128, 255)",
  ];

  const pfcData: PFCData[] = nutrients.map((nutrient, index) => {
    const capitalizedNutrient =
      nutrient.charAt(0).toUpperCase() + nutrient.slice(1);
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
    ] as unknown as Highcharts.SeriesOptions[],
  } as Highcharts.Options);
}

interface FoodIntakes {
  [key: string]: number;
}

function drawFoodintakes(foodintakes: FoodIntakes): void {
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

interface Result {
  status: string;
  pfcRatio: PFCRatio;
  totalNutrientValues: TotalNutrientValues;
  foodIntakes: FoodIntakes;
  message: string;
}

function clearCharts(): void {
  const foodIntakesChart =
    getElementByIdOrThrow<HTMLElement>("food-intakes-chart");
  const pfcRatioChart = getElementByIdOrThrow<HTMLElement>("pfc-ratio-chart");

  foodIntakesChart.textContent = "";
  pfcRatioChart.textContent = "";
}

function handleOptimizationResult(result: Result): void {
  if (result.status === "Optimal") {
    drawPFCRatioWithTotalEnergy(result.pfcRatio, result.totalNutrientValues);
    drawFoodintakes(result.foodIntakes);
  } else {
    clearCharts();
    alert("status: " + result.status + "\n" + "message: " + result.message);
  }
}

export async function optimize(): Promise<void> {
  try {
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

    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }

    const result = await response.json();

    handleOptimizationResult(result);
  } catch (error: unknown) {
    if (error instanceof Error) {
      alert(error.message);
    }
  }
}
