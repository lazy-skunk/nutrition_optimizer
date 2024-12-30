import {
  appendTemplateToTable,
  initializeNutrientSelectOnChange,
  optimize,
} from "./nutrition-optimizer";

import { addEventListenerToActionButton } from "./dom-utilities.js";

document.addEventListener("DOMContentLoaded", () => {
  addEventListenerToActionButton("add-food", () =>
    appendTemplateToTable("food-template", "food-inputs")
  );

  initializeNutrientSelectOnChange();

  addEventListenerToActionButton("add-constraint", () =>
    appendTemplateToTable("constraint-template", "constraint-inputs")
  );

  addEventListenerToActionButton("optimize", () => optimize());
});
