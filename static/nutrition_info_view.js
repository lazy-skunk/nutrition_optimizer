export class NutritionInfoView {
  #tableHeaderId;
  #tableBodyId;

  constructor(tableHeaderId, tableBodyId) {
    this.#tableHeaderId = tableHeaderId;
    this.#tableBodyId = tableBodyId;
  }

  renderTableHeader(headers) {
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

  renderTableBody(rows) {
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
