import { beforeEach, describe, expect, test } from "@jest/globals";
import {
  updateUnitOptions,
  appendTemplateToTable,
} from "../../static/ts/nutrition-optimizer";

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
});
