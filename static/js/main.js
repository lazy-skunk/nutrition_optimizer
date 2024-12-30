import { addEventListenerToActionButton, appendTemplateToTable, initializeNutrientSelectOnChange, optimize, } from "./script.js";
document.addEventListener("DOMContentLoaded", () => {
    addEventListenerToActionButton("add-food", () => appendTemplateToTable("food-template", "food-inputs"));
    initializeNutrientSelectOnChange();
    addEventListenerToActionButton("add-constraint", () => appendTemplateToTable("constraint-template", "constraint-inputs"));
    addEventListenerToActionButton("optimize", () => optimize());
});
//# sourceMappingURL=main.js.map