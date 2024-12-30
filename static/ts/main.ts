import {
  addEventListenerToActionButton,
  appendTemplateToTable,
  setNutrientSelectOnChange,
  optimize,
} from "./script.js";

document.addEventListener("DOMContentLoaded", () => {
  addEventListenerToActionButton("add-food", () =>
    appendTemplateToTable("food-template", "food-inputs")
  );

  setNutrientSelectOnChange();

  addEventListenerToActionButton("add-constraint", () =>
    appendTemplateToTable("constraint-template", "constraint-inputs")
  );

  addEventListenerToActionButton("optimize", () => optimize());
});
