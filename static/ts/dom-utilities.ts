export function getElementByIdOrThrow<T extends HTMLElement>(
  elementId: string
): T {
  const element = document.getElementById(elementId) as T | null;
  if (!element) {
    throw new Error(`Element with ID "${elementId}" not found.`);
  }
  return element;
}

export function getClosestTableRowElementOrThrow(
  element: Element
): HTMLTableRowElement {
  const row = element.closest("tr");
  if (!row) {
    throw new Error("Row element not found.");
  }
  return row;
}

export function getElementByQuerySelectorOrThrow<T extends HTMLElement>(
  parent: Element | Document,
  selector: string
): T {
  const element = parent.querySelector(selector) as T | null;
  if (!element) {
    throw new Error(`Element matching selector "${selector}" not found.`);
  }
  return element;
}

export function getElementsByQuerySelectorAllOrThrow(
  parent: Element,
  selector: string
): NodeListOf<Element> {
  const elements = parent.querySelectorAll(selector);
  if (elements.length == 0) {
    throw new Error(`Element matching selector "${selector}" not found.`);
  }
  return elements;
}
