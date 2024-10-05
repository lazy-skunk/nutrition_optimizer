import { NutritionTableManager } from "./nutrition_table_manager.js";

document.addEventListener("DOMContentLoaded", function () {
  const tableHeaderId = "nutritionTableHeader";
  const tableBodyId = "nutritionTableBody";
  const nutritionTableManager = new NutritionTableManager(
    tableHeaderId,
    tableBodyId
  );

  const NUTRITION_DATA_URL = "static/nutrition_data.json";
  nutritionTableManager.initialize(NUTRITION_DATA_URL);

  document
    .getElementById("searchButton")
    .addEventListener("click", function () {
      const keyword = document.getElementById("searchInput").value;
      nutritionTableManager.filterTable(keyword);
    });
});
