import { beforeEach, describe, expect, test } from "@jest/globals";
import { addItem, removeItem } from "../../static/ts/script";
import { screen } from "@testing-library/dom";

describe("Test addItem function", () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <table>
        <tbody id="test-inputs" data-testid="test-inputs">
          <tr>
            <td>
              <input type="text" />
            </td>
          </tr>
        </tbody>
      </table>
  
      <template id="test-template">
        <tr>
          <td>
            <input type="text" />
          </td>
        </tr>
      </template>
    `;
  });

  test("should clone the template and append it to the target element", () => {
    const templateId = "test-template";
    const targetId = "test-inputs";

    addItem(templateId, targetId);

    const targetElement = screen.getByTestId(targetId);
    expect(targetElement.children.length).toBe(2);
  });

  test("should throw an error if template element is not found", () => {
    const targetId = "test-inputs";

    expect(() => addItem("non-existent-template", targetId)).toThrowError(
      'Template element with ID "non-existent-template" not found.'
    );
  });

  test("should throw an error if target element is not found", () => {
    const templateId = "test-template";

    expect(() => addItem(templateId, "non-existent-target")).toThrowError(
      'Target element with ID "non-existent-target" not found.'
    );
  });
});

describe("Test removeItem function", () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <table>
        <tbody id="test-inputs" data-testid="test-inputs">
          <tr>
            <td>
              <input type="text" />
            </td>
            <td>
              <button type="button" id="remove-button">
                Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <button id="non-tr-button">Remove</button>
    `;
  });

  test("should remove the closest row when a remove button is clicked", () => {
    const button = document.getElementById(
      "remove-button"
    ) as HTMLButtonElement;
    removeItem(button);

    const row = document.querySelector("tr");
    expect(row).toBeNull();
  });

  test("should throw an error if button element is not found", () => {
    const button = screen.queryByText(
      "non-existent-button"
    ) as HTMLButtonElement;

    expect(() => removeItem(button)).toThrowError("Button element not found.");
  });

  test("should throw an error if row element is not found", () => {
    const button = document.getElementById(
      "non-tr-button"
    ) as HTMLButtonElement;

    expect(() => removeItem(button)).toThrowError("Row element not found.");
  });
});
