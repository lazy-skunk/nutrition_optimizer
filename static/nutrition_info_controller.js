export class NutritionInfoController {
  #model;
  #view;
  #currentPage;
  #rowsPerPage;

  constructor(model, view) {
    this.#model = model;
    this.#view = view;
    this.#currentPage = 1;
    this.#rowsPerPage = 10;
  }

  async initialize(url) {
    await this.#model.fetchData(url);
    const originalData = this.#model.getOriginalData();
    if (originalData) {
      this.#view.renderTableHeader(originalData.headers);
      this.#view.renderTableBody(originalData.data.slice(0, this.#rowsPerPage));
      this.#setupPagination(originalData.data.length);
    }
  }

  filterTable(keyword) {
    this.#currentPage = 1;
    const filteredRows = this.#model.getFilteredRows(keyword);
    this.#view.renderTableBody(filteredRows.slice(0, this.#rowsPerPage));
    this.#setupPagination(filteredRows.length);
  }

  #setupPagination(totalRows = this.#model.getOriginalData().data.length) {
    const totalPages = Math.ceil(totalRows / this.#rowsPerPage);
    const paginationElement = document.getElementById("pagination");
    paginationElement.innerHTML = "";

    const maxButtons = 10;
    const halfMax = Math.floor(maxButtons / 2);
    let startPage = Math.max(1, this.#currentPage - halfMax);
    let endPage = Math.min(totalPages, startPage + maxButtons - 1);

    if (totalPages > maxButtons) {
      if (this.#currentPage <= halfMax) {
        endPage = maxButtons;
      } else if (this.#currentPage + halfMax >= totalPages) {
        startPage = totalPages - maxButtons + 1;
      }
    }

    // 「前へ」ボタン
    if (this.#currentPage > 1) {
      const prevLi = document.createElement("li");
      prevLi.classList.add("page-item");
      const prevA = document.createElement("a");
      prevA.classList.add("page-link");
      prevA.textContent = "前へ";
      prevA.href = "#";
      prevA.addEventListener("click", (e) => {
        e.preventDefault();
        this.#currentPage--;
        this.#renderPage(this.#currentPage);
        this.#setupPagination(totalRows);
      });
      prevLi.appendChild(prevA);
      paginationElement.appendChild(prevLi);
    }

    // 「先頭へ」ボタン (ページ数が10以上の場合に表示)
    if (totalPages > maxButtons && this.#currentPage > 1) {
      const firstPageLi = document.createElement("li");
      firstPageLi.classList.add("page-item");
      const firstPageA = document.createElement("a");
      firstPageA.classList.add("page-link");
      firstPageA.textContent = "<< 先頭";
      firstPageA.href = "#";
      firstPageA.addEventListener("click", (e) => {
        e.preventDefault();
        this.#currentPage = 1;
        this.#renderPage(1);
        this.#setupPagination(totalRows);
      });
      firstPageLi.appendChild(firstPageA);
      paginationElement.appendChild(firstPageLi);
    }

    // ページ番号のボタン
    for (let i = startPage; i <= endPage; i++) {
      const li = document.createElement("li");
      li.classList.add("page-item");
      const a = document.createElement("a");
      a.classList.add("page-link");
      a.textContent = i;
      a.href = "#";

      if (i === this.#currentPage) {
        li.classList.add("active");
      }

      a.addEventListener("click", (e) => {
        e.preventDefault();
        this.#currentPage = i;
        this.#renderPage(i);
        this.#setupPagination(totalRows);
      });

      li.appendChild(a);
      paginationElement.appendChild(li);
    }

    // 「末尾へ」ボタン (ページ数が10以上の場合に表示)
    if (totalPages > maxButtons && this.#currentPage < totalPages) {
      const lastPageLi = document.createElement("li");
      lastPageLi.classList.add("page-item");
      const lastPageA = document.createElement("a");
      lastPageA.classList.add("page-link");
      lastPageA.textContent = "末尾 >>";
      lastPageA.href = "#";
      lastPageA.addEventListener("click", (e) => {
        e.preventDefault();
        this.#currentPage = totalPages;
        this.#renderPage(totalPages);
        this.#setupPagination(totalRows);
      });
      lastPageLi.appendChild(lastPageA);
      paginationElement.appendChild(lastPageLi);
    }

    // 「次へ」ボタン
    if (this.#currentPage < totalPages) {
      const nextLi = document.createElement("li");
      nextLi.classList.add("page-item");
      const nextA = document.createElement("a");
      nextA.classList.add("page-link");
      nextA.textContent = "次へ";
      nextA.href = "#";
      nextA.addEventListener("click", (e) => {
        e.preventDefault();
        this.#currentPage++;
        this.#renderPage(this.#currentPage);
        this.#setupPagination(totalRows);
      });
      nextLi.appendChild(nextA);
      paginationElement.appendChild(nextLi);
    }
  }

  #renderPage(pageNumber) {
    const start = (pageNumber - 1) * this.#rowsPerPage;
    const end = start + this.#rowsPerPage;
    const rows = this.#model.getFilteredRows().slice(start, end);
    this.#view.renderTableBody(rows);
  }
}
