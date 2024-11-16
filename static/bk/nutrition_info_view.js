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

    const fragment = document.createDocumentFragment();

    headers.forEach((header) => {
      const headerCell = document.createElement("th");
      headerCell.textContent = header;
      fragment.appendChild(headerCell);
    });

    headerRow.appendChild(fragment);
    tableHeader.appendChild(headerRow);
  }

  renderTableBody(rows) {
    const tableBody = document.getElementById(this.#tableBodyId);
    tableBody.innerHTML = "";

    const fragment = document.createDocumentFragment();

    rows.forEach((rowData) => {
      const tableRow = document.createElement("tr");
      rowData.forEach((cell) => {
        const tableData = document.createElement("td");
        tableData.textContent = cell;
        tableRow.appendChild(tableData);
      });
      fragment.appendChild(tableRow);
    });

    tableBody.appendChild(fragment);
  }

  setupPagination(data) {
    const totalRows = data.length;
    const totalPages = Math.ceil(totalRows / this.#rowsPerPage);
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    const MAX_BUTTONS = 10;
    const halfMax = Math.floor(MAX_BUTTONS / 2);
    let startPage = Math.max(1, this.#currentPage - halfMax);
    let endPage = Math.min(totalPages, startPage + MAX_BUTTONS - 1);

    if (totalPages <= MAX_BUTTONS) {
      startPage = 1;
    } else {
      if (this.#currentPage <= halfMax) {
        endPage = MAX_BUTTONS;
      } else if (this.#currentPage + halfMax >= totalPages) {
        startPage = totalPages - MAX_BUTTONS + 1;
      }
    }

    const fragment = document.createDocumentFragment();

    const SHOW_FIRST_PAGE_BUTTON_THRESHOLD = 6;
    if (
      totalPages > MAX_BUTTONS &&
      this.#currentPage > SHOW_FIRST_PAGE_BUTTON_THRESHOLD
    ) {
      const firstPageLi = this.#createPageButton("<< 先頭へ", 1, data);
      fragment.appendChild(firstPageLi);
    }

    if (this.#currentPage > 1) {
      const prevLi = this.#createPageButton(
        "< 前へ",
        this.#currentPage - 1,
        data
      );
      fragment.appendChild(prevLi);
    }

    for (let i = startPage; i <= endPage; i++) {
      const li = this.#createPageButton(i.toString(), i, data);
      if (i === this.#currentPage) {
        li.classList.add("active");
      }
      fragment.appendChild(li);
    }

    if (this.#currentPage < totalPages) {
      const nextLi = this.#createPageButton(
        "次へ >",
        this.#currentPage + 1,
        data
      );
      fragment.appendChild(nextLi);
    }

    const SHOW_LAST_PAGE_BUTTON_THRESHOLD = totalPages - 4;
    if (
      totalPages > MAX_BUTTONS &&
      this.#currentPage < SHOW_LAST_PAGE_BUTTON_THRESHOLD
    ) {
      const lastPageLi = this.#createPageButton("末尾へ >>", totalPages, data);
      fragment.appendChild(lastPageLi);
    }

    pagination.appendChild(fragment);
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
