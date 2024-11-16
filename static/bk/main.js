import { NutritionInfoModel } from "./nutrition_info_model.js";
import { NutritionInfoView } from "./nutrition_info_view.js";
import { NutritionInfoController } from "./nutrition_info_controller.js";

document.addEventListener("DOMContentLoaded", async function () {
  const nutrition_info_model = new NutritionInfoModel();

  const TABLE_HEADER_ID = "nutritionTableHeader";
  const TABLE_BODY_ID = "nutritionTableBody";
  const nutrition_info_view = new NutritionInfoView(
    TABLE_HEADER_ID,
    TABLE_BODY_ID
  );

  const controller = new NutritionInfoController(
    nutrition_info_model,
    nutrition_info_view
  );

  const NUTRITION_DATA_URL = "static/nutrition_data.json";
  await controller.initialize(NUTRITION_DATA_URL);

  document
    .getElementById("searchInput")
    .addEventListener("keyup", function (event) {
      if (event.key === "Enter") {
        const keyword = document.getElementById("searchInput").value;
        controller.filterTable(keyword);
      }
    });

  document
    .getElementById("searchButton")
    .addEventListener("click", function () {
      const keyword = document.getElementById("searchInput").value;
      controller.filterTable(keyword);
    });
});
