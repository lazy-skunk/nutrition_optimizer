async function fetchData(url) {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      throw new Error(`Network response was not ok: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("There was a problem with the fetch operation:", error);
  }
}

function renderTableBody(tableData, tableBodyId) {
  const tableBody = document.getElementById(tableBodyId);

  tableData.forEach((rowData) => {
    const tr = document.createElement("tr");

    rowData.forEach((cell) => {
      const td = document.createElement("td");
      td.textContent = cell;
      tr.appendChild(td);
    });

    tableBody.appendChild(tr);
  });
}

function filterTableByKeyword(keyword, tableId) {
  const table = document.getElementById(tableId);
  const rows = table.getElementsByTagName("tr");

  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].getElementsByTagName("td");
    let matched = false;

    for (let j = 0; j < cells.length; j++) {
      if (cells[j].textContent.includes(keyword)) {
        matched = true;
        break;
      }
    }

    rows[i].style.display = matched ? "" : "none";
  }
}

document.addEventListener("DOMContentLoaded", function () {
  const NUTRITION_DATA_URL = "static/nutrition_data.json";
  fetchData(NUTRITION_DATA_URL).then((nutrition_data) => {
    if (nutrition_data) {
      const tableBodyId = "nutritionTableBody";
      renderTableBody(nutrition_data, tableBodyId);
    }
  });

  document
    .getElementById("searchButton")
    .addEventListener("click", function () {
      const keyword = document.getElementById("searchInput").value;
      const tableId = "nutritionTable";
      filterTableByKeyword(keyword, tableId);
    });
});
