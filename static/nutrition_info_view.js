export class NutritionInfoView {
  #tableHeaderId;
  #tableBodyId;
  #currentPage;
  #rowsPerPage;

  constructor(tableHeaderId, tableBodyId) {
    this.#tableHeaderId = tableHeaderId;
    this.#tableBodyId = tableBodyId;
    this.#currentPage = 1;
    this.#rowsPerPage = 10;
  }

  get rowsPerPage() {
    return this.#rowsPerPage;
  }

  get currentPage() {
    return this.#currentPage;
  }

  set currentPage(value) {
    this.#currentPage = value;
  }

  renderTableHeader(headers) {
    const tableHeader = document.getElementById(this.#tableHeaderId);
    tableHeader.innerHTML = "";
    const headerRow = document.createElement("tr");

    headers.forEach((header) => {
      const headerCell = document.createElement("th");
      headerCell.textContent = header;
      headerRow.appendChild(headerCell);
    });

    tableHeader.appendChild(headerRow);
  }

  renderTableBody(rows) {
    const tableBody = document.getElementById(this.#tableBodyId);
    tableBody.innerHTML = "";

    rows.forEach((rowData) => {
      const tableRow = document.createElement("tr");
      rowData.forEach((cell) => {
        const tableData = document.createElement("td");
        tableData.textContent = cell;
        tableRow.appendChild(tableData);
      });
      tableBody.appendChild(tableRow);
    });
  }

  setupPagination(data) {
    const totalRows = data.length;
    const totalPages = Math.ceil(totalRows / this.#rowsPerPage);
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    const maxButtons = 10;
    const halfMax = Math.floor(maxButtons / 2);
    let startPage = Math.max(1, this.#currentPage - halfMax);
    let endPage = Math.min(totalPages, startPage + maxButtons - 1);

    if (totalPages <= maxButtons) {
      startPage = 1;
    } else {
      if (this.#currentPage <= halfMax) {
        endPage = maxButtons;
      } else if (this.#currentPage + halfMax >= totalPages) {
        startPage = totalPages - maxButtons + 1;
      }
    }

    if (totalPages > maxButtons && this.#currentPage > 1) {
      const firstPageLi = this.#createPageButton("<< 先頭へ", 1, data);
      pagination.appendChild(firstPageLi);
    }

    if (this.#currentPage > 1) {
      const prevLi = this.#createPageButton(
        "< 前へ",
        this.#currentPage - 1,
        data
      );
      pagination.appendChild(prevLi);
    }

    for (let i = startPage; i <= endPage; i++) {
      const li = this.#createPageButton(i.toString(), i, data);
      if (i === this.#currentPage) {
        li.classList.add("active");
      }
      pagination.appendChild(li);
    }

    if (this.#currentPage < totalPages) {
      const nextLi = this.#createPageButton(
        "次へ >",
        this.#currentPage + 1,
        data
      );
      pagination.appendChild(nextLi);
    }

    if (totalPages > maxButtons && this.#currentPage < totalPages) {
      const lastPageLi = this.#createPageButton("末尾へ >>", totalPages, data);
      pagination.appendChild(lastPageLi);
    }
  }

  #createPageButton(text, pageNumber, data) {
    const li = document.createElement("li");
    li.classList.add("page-item");
    const a = document.createElement("a");
    a.classList.add("page-link");
    a.textContent = text;
    a.href = "#";

    a.addEventListener("click", (event) => {
      event.preventDefault();
      this.#currentPage = pageNumber;
      this.#renderPage(pageNumber, data);
    });

    li.appendChild(a);
    return li;
  }

  #renderPage(pageNumber, data) {
    const start = (pageNumber - 1) * this.#rowsPerPage;
    const end = start + this.#rowsPerPage;
    const rows = data.slice(start, end);
    this.renderTableBody(rows);
    this.setupPagination(data);
  }
}
