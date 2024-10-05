export class NutritionTableManager {
  #tableHeaderId;
  #tableBodyId;
  #originalData;

  constructor(tableHeaderId, tableBodyId) {
    this.#tableHeaderId = tableHeaderId;
    this.#tableBodyId = tableBodyId;
    this.#originalData = null;
  }

  async initialize(url) {
    await this.#fetchData(url);
    if (this.#originalData) {
      this.#renderTable();
    }
  }

  filterTable(keyword) {
    const filteredRows = this.#originalData.data.filter((row) =>
      row.some((cell) => String(cell).includes(keyword))
    );
    this.#renderTableBody(filteredRows);
  }

  async #fetchData(url) {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }

      this.#originalData = await response.json();
    } catch (error) {
      console.error("There was a problem with the fetch operation:", error);
    }
  }

  #renderTable() {
    const headers = this.#originalData.headers;
    const rows = this.#originalData.data;

    this.#renderTableHeader(headers);
    this.#renderTableBody(rows);
  }

  #renderTableHeader(headers) {
    const tableHeader = document.getElementById(this.#tableHeaderId);
    tableHeader.innerHTML = "";
    const headerRow = document.createElement("tr");

    headers.forEach((header) => {
      const th = document.createElement("th");
      th.textContent = header;
      headerRow.appendChild(th);
    });

    tableHeader.appendChild(headerRow);
  }

  #renderTableBody(rows) {
    const tableBody = document.getElementById(this.#tableBodyId);
    tableBody.innerHTML = "";

    rows.forEach((rowData) => {
      const tr = document.createElement("tr");
      rowData.forEach((cell) => {
        const td = document.createElement("td");
        td.textContent = cell;
        tr.appendChild(td);
      });
      tableBody.appendChild(tr);
    });
  }
}
