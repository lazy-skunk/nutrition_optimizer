export function getElementByIdOrThrow(elementId) {
    const element = document.getElementById(elementId);
    if (!element) {
        throw new Error(`Element with ID "${elementId}" not found.`);
    }
    return element;
}
export function getClosestTableRowElementOrThrow(element) {
    const row = element.closest("tr");
    if (!row) {
        throw new Error("Row element not found.");
    }
    return row;
}
export function getElementByQuerySelectorOrThrow(parent, selector) {
    const element = parent.querySelector(selector);
    if (!element) {
        throw new Error(`Element matching selector "${selector}" not found.`);
    }
    return element;
}
export function getElementsByQuerySelectorAllOrThrow(parent, selector) {
    const elements = parent.querySelectorAll(selector);
    if (elements.length == 0) {
        throw new Error(`Element matching selector "${selector}" not found.`);
    }
    return elements;
}
export function addEventListenerToActionButton(buttonId, callbackFunction) {
    const button = getElementByIdOrThrow(buttonId);
    button.addEventListener("click", callbackFunction);
}
//# sourceMappingURL=dom-utilities.js.map