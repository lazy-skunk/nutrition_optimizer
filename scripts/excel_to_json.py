import pandas as pd


def excel_to_json(excel_file_path: str, json_file_path: str) -> None:
    df = pd.read_excel(excel_file_path)

    json_data = df.to_json(orient="values", force_ascii=False)

    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json_file.write(json_data)


if __name__ == "__main__":
    _EXCEL_FILE_PATH = "data/minimal.xlsx"
    _JSON_FILE_PATH = "static/nutrition_data.json"

    excel_to_json(_EXCEL_FILE_PATH, _JSON_FILE_PATH)
