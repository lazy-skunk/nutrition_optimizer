import json

import pandas as pd

_EXCEL_FILE_PATH = "data/minimal.xlsx"
_JSON_FILE_PATH = "static/nutrition_data.json"


def excel_to_json(excel_file_path: str, json_file_path: str) -> None:
    df = pd.read_excel(excel_file_path)

    headers = df.columns.tolist()
    data = df.values.tolist()
    json_data = {"headers": headers, "data": data}

    with open(json_file_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, ensure_ascii=False)


if __name__ == "__main__":
    excel_to_json(_EXCEL_FILE_PATH, _JSON_FILE_PATH)
