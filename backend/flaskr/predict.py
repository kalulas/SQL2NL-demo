from flask import Blueprint, request, redirect, current_app, jsonify
from flaskr import sql2text_bridge, utils, file_utils
from flask_request_id import RequestID

bp = Blueprint('predict', __name__, url_prefix="/predict")
# bp.record_once(sql2text_bridge.setup_checkpoints)
# bp.record_once(sql2text_bridge.setup_models)

def setup_bridge_if_not_ready():
    if sql2text_bridge.is_ready():
        return
    
    current_app.logger.info("bridge not ready, setup checkpoints and models...")
    sql2text_bridge.setup_checkpoints(True)
    sql2text_bridge.setup_models(True)
    current_app.logger.info("bridge is now ready!")


@bp.route('/', methods=('GET', 'POST'))
def predict_index():
    request_ext = RequestID(current_app)
    current_app.logger.critical("RequestID is %s", request_ext.id)
    
    # identifier = utils.generate_request_id(request.remote_addr)
    identifier = request_ext.id
    if request.method == 'GET':
        return redirect('/../') # to home page
    
    if request.method == 'POST':
        selected_models = request.json['selected']
        input_sql = request.json['sql']
        # this is seperated by '\n'
        gold_nl_array = request.json['gold_nl']
        db_id = request.json['db_id']
        current_app.logger.info("request info: '%s'", request.json)
        # current_app.logger.info("request selected_models: %s", selected_models)

        setup_bridge_if_not_ready()

        results = []
        for model in selected_models:
            result = sql2text_bridge.predict(model, db_id, gold_nl_array, input_sql, identifier)
            results.append(result.toDict())
            # result = result + prediction

        return jsonify(results)

@bp.route('/models/', methods=['POST'])
def process_models_request():
    available_models = sql2text_bridge.SUPPORTED_MODELS
    return jsonify(available_models)

@bp.route('/databases/', methods=['POST'])
def process_databases_request():
    available_database_names = file_utils.get_databases_from_file(sql2text_bridge.TRAIN_TABLE_FILE_PATH)
    # current_app.logger.info(available_database_names)
    return jsonify(available_database_names)
