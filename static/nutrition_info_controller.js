export class NutritionInfoController {
  #model;
  #view;

  constructor(model, view) {
    this.#model = model;
    this.#view = view;
  }

  async initialize(url) {
    await this.#model.fetchData(url);
    const originalData = this.#model.getOriginalData();
    if (originalData) {
      this.#view.renderTableHeader(originalData.headers);
      this.#view.renderTableBody(
        originalData.data.slice(0, this.#view.rowsPerPage)
      );
      this.#view.setupPagination(originalData.data);
    }
  }

  filterTable(keyword) {
    this.#view.currentPage = 1;
    const filteredRows = this.#model.getFilteredRows(keyword);
    this.#view.renderTableBody(filteredRows.slice(0, this.#view.rowsPerPage));
    this.#view.setupPagination(filteredRows);
  }
}
