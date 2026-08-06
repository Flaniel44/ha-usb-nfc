import json


def read_options() -> dict:
    try:
        with open("/data/options.json", "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
