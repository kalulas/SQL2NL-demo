from flask import Blueprint, request, redirect, current_app
from flaskr import sql2text_bridge

bp = Blueprint('predict', __name__, url_prefix="/predict")

@bp.route('/', methods=('GET', 'POST'))
def predict_index():
    if request.method == 'GET':
        return redirect('/../') # to home page
    
    if request.method == 'POST':
        selected_models = request.json['selected']
        input_sql = request.json['sql'].upper()
        current_app.logger.info("request input_sql: '%s'", input_sql)
        current_app.logger.info("request selected_models: %s", selected_models)
        result = ""
        for model in selected_models:
            result = result + sql2text_bridge.predict(model, input_sql)

        return result #TODO
