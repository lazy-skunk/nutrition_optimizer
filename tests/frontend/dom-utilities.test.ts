import { beforeEach, describe, expect, test, jest } from "@jest/globals";
import {
  getElementByIdOrThrow,
  getClosestTableRowElementOrThrow,
  getElementByQuerySelectorOrThrow,
  getElementsByQuerySelectorAllOrThrow,
  addEventListenerToActionButton,
} from "../../static/ts/dom-utilities.ts";

describe("DOM Utilities", () => {
  beforeEach(() => {
    document.body.innerHTML = `
    <div>
      <table id="test-table">
        <tr>
          <td><input type="number" /></td>
          <td><button id="remove-item">Remove Item</button></td>
        </tr>
      </table>
      <button id="add-item-id" name="add-item-name">Add Item</button>
    </div>
    `;
  });

  describe("getElementByIdOrThrow", () => {
    test("should return the element when it exists", () => {
      const element = getElementByIdOrThrow("add-item-id");
      expect(element).not.toBeNull();
      expect(element.id).toBe("add-item-id");
    });

    test("should throw an error when the element does not exist", () => {
      expect(() => getElementByIdOrThrow("non-existent-id")).toThrowError(
        'Element with ID "non-existent-id" not found.'
      );
    });
  });

  describe("getClosestTableRowElementOrThrow", () => {
    test("should return the closest tr element", () => {
      const button = document.getElementById(
        "remove-item"
      ) as HTMLButtonElement;
      const row = getClosestTableRowElementOrThrow(button);
      expect(row.tagName).toBe("TR");
    });

    test("should throw an error if there is no tr element", () => {
      const button = document.getElementById(
        "add-item-id"
      ) as HTMLButtonElement;
      expect(() => getClosestTableRowElementOrThrow(button)).toThrowError(
        "Row element not found."
      );
    });
  });

  describe("getElementByQuerySelectorOrThrow", () => {
    test("should return the element when it exists", () => {
      const element = getElementByQuerySelectorOrThrow(
        document,
        "[name='add-item-name']"
      );
      expect(element).not.toBeNull();
      expect(element.id).toBe("add-item-id");
    });

    test("should throw an error when the element does not exist", () => {
      expect(() =>
        getElementByQuerySelectorOrThrow(document, "#non-existent-id")
      ).toThrowError('Element matching selector "#non-existent-id" not found.');
    });
  });

  describe("getElementsByQuerySelectorAllOrThrow", () => {
    test("should return a non-empty NodeList", () => {
      const element = getElementByIdOrThrow("test-table");
      const elements = getElementsByQuerySelectorAllOrThrow(element, "tr");
      expect(elements.length).toBeGreaterThan(0);
    });

    test("should throw an error if no elements are found", () => {
      const element = getElementByIdOrThrow("test-table");
      expect(() =>
        getElementsByQuerySelectorAllOrThrow(element, ".non-existent")
      ).toThrowError('Element matching selector ".non-existent" not found.');
    });
  });

  describe("addEventListenerToActionButton", () => {
    test("should add event listener to button and call callback on click", () => {
      const mockCallback = jest.fn();
      addEventListenerToActionButton("add-item-id", mockCallback);

      const button = document.getElementById(
        "add-item-id"
      ) as HTMLButtonElement;
      button.click();

      expect(mockCallback).toHaveBeenCalledTimes(1);
    });

    test("should throw error if button does not exist", () => {
      const mockCallback = jest.fn();
      expect(() =>
        addEventListenerToActionButton("non-existent-button", mockCallback)
      ).toThrowError('Element with ID "non-existent-button" not found.');
    });
  });
});
