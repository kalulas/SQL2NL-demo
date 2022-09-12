import json
from flask import current_app
from typing import List

input_sql_json_dir = "SavedData/sql2text/"

def get_input_sql_element(db_id:str, gold_nl:str, input_sql:str) -> dict:
    return {
        "db_id": db_id,
        "orig_query": input_sql,
        "keywords": [
            "all"
        ],
        "query": "",
        "question": gold_nl
    }

def build_input_sql_json(db_id:str, gold_nl_array_str:str, input_sql:str, filename:str) -> str:
    """
    return relative filepath if file successfully created, empty string if failed
    """
    filepath = input_sql_json_dir + filename + ".json"
    data = []
    gold_nl_array = gold_nl_array_str.split('\n')
    for gold_nl in gold_nl_array:
        data.append(get_input_sql_element(db_id, gold_nl, input_sql))
    
    current_app.logger.info(f"testset with {len(data)} questions is created")
    fp = open(filepath, 'w')
    if fp is None:
        current_app.logger.error(f"open {filepath} failed, exit")
        return ""

    json.dump(data, fp, indent=4)
    current_app.logger.info("file %s is created", filepath)
    return filepath


def get_databases_from_file(file_path:str) -> List[str]:
    result = []
    with open(file_path, 'r') as fp:
        db_list = json.load(fp)
        for db_config in db_list:
            if "db_id" not in db_config.keys():
                current_app.logger.error(f" 'db_id' not found in {file_path}")
                continue

            result.append(db_config["db_id"])

    return result
