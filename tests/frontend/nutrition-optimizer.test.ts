import { beforeEach, describe, expect, test } from "@jest/globals";
import { updateUnitOptions } from "../../static/ts/nutrition-optimizer.ts";

describe("Nutrition Optimizer", () => {
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

  describe("updateUnitOptions", () => {
    test("should update unit options when nutrient select value is 'energy'", () => {
      const row = document.querySelector("tr") as HTMLTableRowElement;
      const nutrientSelect = row.querySelector(
        "[name='constraint-nutrient']"
      ) as HTMLSelectElement;
      const unitSelect = row.querySelector(
        "[name='constraint-unit']"
      ) as HTMLSelectElement;

      nutrientSelect.value = "energy";
      updateUnitOptions(nutrientSelect);

      expect(unitSelect.disabled).toBe(true);

      const options = unitSelect.querySelectorAll("option");
      expect(options.length).toBeGreaterThan(0);
      expect(options[0].value).toBe("energy");
    });

    test("should update unit options when nutrient select value is not 'energy'", () => {
      const row = document.querySelector("tr") as HTMLTableRowElement;
      const nutrientSelect = row.querySelector(
        "[name='constraint-nutrient']"
      ) as HTMLSelectElement;
      const unitSelect = row.querySelector(
        "[name='constraint-unit']"
      ) as HTMLSelectElement;

      nutrientSelect.value = "protein";
      updateUnitOptions(nutrientSelect);

      expect(unitSelect.disabled).toBe(false);

      const options = unitSelect.querySelectorAll("option");
      expect(options.length).toBeGreaterThan(1);
      expect(options[0].value).toBe("amount");
      expect(options[1].value).toBe("ratio");
    });
  });
});
