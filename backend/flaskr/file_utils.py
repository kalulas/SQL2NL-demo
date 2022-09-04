import json
from flask import current_app

input_sql_json_dir = "SavedData/sql2text/"

def get_input_sql_element(input_sql:str) -> dict:
    return {
        "db_id": "concert_singer",
        "orig_query": input_sql,
        "keywords": [
            "all"
        ],
        "query": "",
        "question": ""
    }

def build_input_sql_json(input_sql:str, filename:str) -> str:
    """
    return relative filepath if file successfully created, empty string if failed
    """
    filepath = input_sql_json_dir + filename + ".json"
    data = []
    data.append(get_input_sql_element(input_sql))
    fp = open(filepath, 'w')
    if fp is None:
        current_app.logger.error(f"open {filepath} failed, exit")
        return ""

    json.dump(data, fp, indent=4)
    current_app.logger.info("file %s is created", filepath)
    return filepath
