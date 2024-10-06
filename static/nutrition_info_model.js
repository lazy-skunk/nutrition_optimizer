export class NutritionInfoModel {
  #originalData;

  constructor() {
    this.#originalData = null;
  }

  async fetchData(url) {
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

  getFilteredRows(keyword = null) {
    if (keyword) {
      return this.#originalData.data.filter((row) =>
        row.some((cell) => String(cell).includes(keyword))
      );
    }
    return this.#originalData.data;
  }

  getOriginalData() {
    return this.#originalData;
  }
}
