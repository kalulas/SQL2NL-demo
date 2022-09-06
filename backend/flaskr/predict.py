from flask import Blueprint, request, redirect, current_app
from flaskr import sql2text_bridge, utils
from flask_request_id import RequestID

bp = Blueprint('predict', __name__, url_prefix="/predict")
# bp.record_once(sql2text_bridge.setup_checkpoints)
# bp.record_once(sql2text_bridge.setup_models)

@bp.before_app_first_request
def setup_bridge():
    sql2text_bridge.setup_checkpoints(True)
    sql2text_bridge.setup_models(True)

@bp.route('/', methods=('GET', 'POST'))
def predict_index():
    request_ext = RequestID(current_app)
    current_app.logger.critical("RequestID is %s", request_ext.id)
    
    identifier = utils.generate_request_id(request.remote_addr)
    if request.method == 'GET':
        return redirect('/../') # to home page
    
    if request.method == 'POST':
        selected_models = request.json['selected']
        input_sql = request.json['sql']
        current_app.logger.info("request input_sql: '%s'", input_sql)
        current_app.logger.info("request selected_models: %s", selected_models)
        result = ""
        for model in selected_models:
            prediction, success = sql2text_bridge.predict(model, input_sql, identifier)
            result = result + prediction

        return result
