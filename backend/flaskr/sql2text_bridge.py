from flask import current_app
from Model.model import RelativeTransformer
import torch

def predict(model:str, input_sql:str):
    current_app.logger.info(f"you are on bridge, torch version:{torch.__version__}")
    return f"[{model}] {input_sql}\n"