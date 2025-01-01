import {
  beforeEach,
  describe,
  expect,
  test,
  jest,
  afterEach,
} from "@jest/globals";
import {
  updateUnitOptions,
  appendTemplateToTable,
  initializeNutrientSelectOnChange,
  optimize,
} from "../../static/ts/nutrition-optimizer";
import Highcharts from "highcharts";
window.Highcharts = Highcharts;

describe("Nutrition Optimizer", () => {
  describe("updateUnitOptions", () => {
    beforeEach(() => {
      document.body.innerHTML = `
        <table id="constraint-table">
          <tbody id="constraint-inputs">
            <tr>
              <td>
                <select class="form-select" name="constraint-nutrient">
                  <option value="energy">Energy</option>
                  <option value="protein">Protein</option>
                  <option value="fat">Fat</option>
                  <option value="carbohydrates">Carbohydrates</option>
                </select>
              </td>
              <td>
                <select class="form-select" name="constraint-unit" disabled>
                  <option value="energy">kcal</option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>

        <template id="unit-options-energy">
          <option value="energy">kcal</option>
        </template>

        <template id="unit-options-amount-ratio">
          <option value="amount">g</option>
          <option value="ratio">%</option>
        </template>
      `;
    });

    test("should update unit options when nutrient select value is 'energy'", () => {
      // Arrange
      const row = document.querySelector("tr") as HTMLTableRowElement;
      const nutrientSelect = row.querySelector(
        "[name='constraint-nutrient']"
      ) as HTMLSelectElement;
      const unitSelect = row.querySelector(
        "[name='constraint-unit']"
      ) as HTMLSelectElement;

      nutrientSelect.value = "energy";
      // Act
      updateUnitOptions(nutrientSelect);

      // Assert
      expect(unitSelect.disabled).toBe(true);

      const options = unitSelect.querySelectorAll("option");
      expect(options.length).toBe(1);
      expect(options[0].value).toBe("energy");
    });

    test("should update unit options when nutrient select value is not 'energy'", () => {
      // Arrange
      const row = document.querySelector("tr") as HTMLTableRowElement;
      const nutrientSelect = row.querySelector(
        "[name='constraint-nutrient']"
      ) as HTMLSelectElement;
      const unitSelect = row.querySelector(
        "[name='constraint-unit']"
      ) as HTMLSelectElement;

      nutrientSelect.value = "protein";

      // Act
      updateUnitOptions(nutrientSelect);

      // Assert
      expect(unitSelect.disabled).toBe(false);

      const options = unitSelect.querySelectorAll("option");
      expect(options.length).toBe(2);
      expect(options[0].value).toBe("amount");
      expect(options[1].value).toBe("ratio");
    });
  });

  describe("appendTemplateToTable", () => {
    beforeEach(() => {
      document.body.innerHTML = `
        <table id="food-table">
          <tbody id="food-inputs">
            <tr>
              <td>
                <input type="text" class="form-control" name="food-name" />
              </td>
              <td class="no-action"></td>
            </tr>
          </tbody>
        </table>

        <button type="button" id="add-food" class="btn btn-outline-primary">
          Add Food
        </button>

        <table id="constraint-table">
          <tbody id="constraint-inputs">
            <tr>
              <td>
                <select class="form-select" name="constraint-nutrient">
                  <option value="energy">Energy</option>
                  <option value="protein">Protein</option>
                  <option value="fat">Fat</option>
                  <option value="carbohydrates">Carbohydrates</option>
                </select>
              </td>
              <td>
                <select class="form-select" name="constraint-unit" disabled>
                  <option value="energy">kcal</option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>

        <button type="button" id="add-constraint" class="btn btn-outline-primary">
          Add Constraint
        </button>

        <template id="food-template">
          <tr>
            <td>
              <input type="text" class="form-control" name="food-name" />
            </td>
            <td>
              <button type="button" class="btn btn-outline-danger">Remove</button>
            </td>
          </tr>
        </template>

        <template id="constraint-template">
          <tr>
            <td>
              <select class="form-select" name="constraint-nutrient">
                <option value="energy">Energy</option>
                <option value="protein">Protein</option>
                <option value="fat">Fat</option>
                <option value="carbohydrates">Carbohydrates</option>
              </select>
            </td>
            <td>
              <select class="form-select" name="constraint-unit" disabled>
                <option value="energy">kcal</option>
              </select>
            </td>
            <td>
              <button class="btn btn-outline-danger">Remove</button>
            </td>
          </tr>
        </template>

        <template id="unit-options-energy">
          <option value="energy">kcal</option>
        </template>

        <template id="unit-options-amount-ratio">
          <option value="amount">g</option>
          <option value="ratio">%</option>
        </template>
      `;
    });

    test("should append food template", () => {
      // Arrange
      const templateId = "food-template";
      const targetId = "food-inputs";

      // Act
      appendTemplateToTable(templateId, targetId);

      // Assert
      const rows = document.querySelectorAll("#food-inputs tr");
      expect(rows.length).toBe(2);
    });

    test("should remove the food row when remove button is clicked", () => {
      // Arrange
      const templateId = "food-template";
      const targetId = "food-inputs";
      appendTemplateToTable(templateId, targetId);

      const appendedRow = document.querySelector(
        "#food-inputs tr:last-child"
      ) as HTMLTableRowElement;
      const removeButton = appendedRow.querySelector(
        "button"
      ) as HTMLButtonElement;

      // Act
      removeButton.click();

      // Assert
      const rowsAfterRemove = document.querySelectorAll("#food-inputs tr");
      expect(rowsAfterRemove.length).toBe(1);
    });

    test("should append constraint template", () => {
      // Arrange
      const templateId = "constraint-template";
      const targetId = "constraint-inputs";

      // Act
      appendTemplateToTable(templateId, targetId);

      // Assert
      const rowsBeforeRemoveRow = document.querySelectorAll(
        "#constraint-inputs tr"
      );
      expect(rowsBeforeRemoveRow.length).toBe(2);
    });

    test("should update unit options when nutrient select value is 'protein'", () => {
      // Arrange
      const templateId = "constraint-template";
      const targetId = "constraint-inputs";

      appendTemplateToTable(templateId, targetId);

      const row = document.querySelector(
        "#constraint-inputs tr:last-child"
      ) as HTMLTableRowElement;
      const nutrientSelect = row.querySelector(
        "[name='constraint-nutrient']"
      ) as HTMLSelectElement;
      nutrientSelect.value = "protein";

      // Act
      nutrientSelect.dispatchEvent(new Event("change"));

      // Assert
      const unitSelect = row.querySelector(
        "[name='constraint-unit']"
      ) as HTMLSelectElement;

      expect(unitSelect.disabled).toBe(false);
      const options = unitSelect.querySelectorAll("option");
      expect(options.length).toBe(2);
      expect(options[0].value).toBe("amount");
      expect(options[1].value).toBe("ratio");
    });

    test("should remove the constraint row when remove button is clicked", () => {
      // Arrange
      const templateId = "constraint-template";
      const targetId = "constraint-inputs";

      appendTemplateToTable(templateId, targetId);

      const row = document.querySelector(
        "#constraint-inputs tr:last-child"
      ) as HTMLTableRowElement;
      const removeButton = row.querySelector("button") as HTMLButtonElement;

      // Act
      removeButton.click();

      // Assert
      const rowsAfterRemove = document.querySelectorAll(
        "#constraint-inputs tr"
      );
      expect(rowsAfterRemove.length).toBe(1);
    });
  });

  describe("initializeNutrientSelectOnChange", () => {
    beforeEach(() => {
      document.body.innerHTML = `
        <table id="constraint-table">
          <tbody id="constraint-inputs">
            <tr>
              <td>
                <select class="form-select" name="constraint-nutrient">
                  <option value="energy">Energy</option>
                  <option value="protein">Protein</option>
                  <option value="fat">Fat</option>
                  <option value="carbohydrates">Carbohydrates</option>
                </select>
              </td>
              <td>
                <select class="form-select" name="constraint-unit" disabled>
                  <option value="energy">kcal</option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>

        <template id="unit-options-energy">
          <option value="energy">kcal</option>
        </template>

        <template id="unit-options-amount-ratio">
          <option value="amount">g</option>
          <option value="ratio">%</option>
        </template>
      `;
    });

    test("should initialize nutrient select with change event listener", () => {
      // Arrange
      initializeNutrientSelectOnChange();

      const nutrientSelect = document.querySelector(
        "[name='constraint-nutrient']"
      ) as HTMLSelectElement;
      nutrientSelect.value = "protein";

      // Act
      nutrientSelect.dispatchEvent(new Event("change"));

      // Assert
      const unitSelect = document.querySelector(
        "[name='constraint-unit']"
      ) as HTMLSelectElement;

      expect(unitSelect.disabled).toBe(false);

      const options = unitSelect.querySelectorAll("option");
      expect(options.length).toBe(2);
      expect(options[0].value).toBe("amount");
      expect(options[1].value).toBe("ratio");
    });
  });

  describe("optimize", () => {
    let originalFetch: typeof fetch;

    beforeEach(() => {
      originalFetch = global.fetch;
      global.fetch = jest.fn() as jest.MockedFunction<typeof fetch>;

      document.body.innerHTML = `
        <table class="table table-bordered table-striped" id="food-table">
          <tbody id="food-inputs">
            <tr>
              <td>
                <input type="text" class="form-control" name="food-name" />
              </td>
              <td>
                <input type="number" class="form-control" name="food-energy" />
              </td>
              <td>
                <input type="number" class="form-control" name="food-protein" />
              </td>
              <td>
                <input type="number" class="form-control" name="food-fat" />
              </td>
              <td>
                <input type="number" class="form-control" name="food-carbohydrates" />
              </td>
              <td>
                <input type="number" class="form-control" name="food-grams-per-unit" />
              </td>
              <td>
                <input type="number" class="form-control" name="food-minimum-intake" />
              </td>
              <td>
                <input type="number" class="form-control" name="food-maximum-intake" />
              </td>
            </tr>
          </tbody>
        </table>

        <table class="table table-bordered table-striped" id="objective-table">
          <tbody id="objective-input">
            <tr>
              <td>
                <select class="form-select" name="objective-sense">
                  <option value="minimize">Minimize</option>
                  <option value="maximize" selected>Maximize</option>
                </select>
              </td>
              <td>
                <select class="form-select" name="objective-nutrient">
                  <option value="energy">Energy</option>
                  <option value="protein">Protein</option>
                  <option value="fat">Fat</option>
                  <option value="carbohydrates">Carbohydrates</option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>

        <table>
          <tbody id="constraint-inputs">
            <tr>
              <td>
                <select class="form-select" name="constraint-min-max">
                  <option value="min">Minimum</option>
                  <option value="max">Maximum</option>
                </select>
              </td>
              <td>
                <select class="form-select" name="constraint-nutrient">
                  <option value="energy">Energy</option>
                  <option value="protein">Protein</option>
                  <option value="fat">Fat</option>
                  <option value="carbohydrates">Carbohydrates</option>
                </select>
              </td>
              <td>
                <select class="form-select" name="constraint-unit" disabled>
                  <option value="energy">kcal</option>
                </select>
              </td>
              <td>
                <input type="number" class="form-control" name="constraint-value" />
              </td>
            </tr>
          </tbody>
        </table>

        <div id="food-intakes-chart"></div>
     
        <div id="pfc-ratio-chart"></div>
      `;
    });

    afterEach(() => {
      global.fetch = originalFetch;
      jest.clearAllMocks();
    });

    test("should update charts with optimization result when status is 'Optimal'", async () => {
      // Arrange
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        json: () =>
          Promise.resolve({
            status: "Optimal",
            pfcRatio: { protein: 34.5, fat: 64.6, carbohydrates: 0.8 },
            totalNutrientValues: {
              energy: 134,
              protein: 12.5,
              fat: 10.4,
              carbohydrates: 0.3,
            },
            foodIntakes: { boiled_egg: 1 },
            message: "",
          }),
      } as never);

      // Act
      await optimize();

      // Assert
      const foodIntakesChart = document.getElementById(
        "food-intakes-chart"
      ) as HTMLElement;
      const pfcRatioChart = document.getElementById(
        "pfc-ratio-chart"
      ) as HTMLElement;

      expect(foodIntakesChart.innerHTML).not.toBe("");
      expect(pfcRatioChart.innerHTML).not.toBe("");
    });

    test("bbb", async () => {
      // Arrange
      (global.fetch as jest.Mock).mockResolvedValueOnce({
        json: () =>
          Promise.resolve({
            status: "Infeasible",
            message: "test message",
          }),
      } as never);

      global.alert = jest.fn();

      // Act
      await optimize();

      // Assert
      const foodIntakesChart = document.getElementById(
        "food-intakes-chart"
      ) as HTMLElement;
      const pfcRatioChart = document.getElementById(
        "pfc-ratio-chart"
      ) as HTMLElement;

      expect(foodIntakesChart.innerHTML).toBe("");
      expect(pfcRatioChart.innerHTML).toBe("");

      expect(global.alert).toHaveBeenCalledWith(
        "status: Infeasible\nmessage: test message"
      );
    });
  });
});
