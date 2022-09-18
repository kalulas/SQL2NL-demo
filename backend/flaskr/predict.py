from flask import Blueprint, request, redirect, current_app, jsonify
from flaskr import utils
from flaskr.evaluation_result import EvaluationResult

bp = Blueprint('predict', __name__, url_prefix="/predict")
# bp.record_once(sql2text_bridge.setup_checkpoints)
# bp.record_once(sql2text_bridge.setup_models)


@bp.route('/', methods=('GET', 'POST'))
def predict_index():
    identifier = utils.generate_request_id(request.remote_addr)
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

        results = []
        for model in selected_models:
            # result = sql2text_bridge.predict(model, db_id, gold_nl_array, input_sql, identifier)
            result = EvaluationResult()
            result.modelName = model
            result.original = input_sql
            result.failedReason = 'pytorch not available on this branch'

            results.append(result.toDict())
            # result = result + prediction

        return jsonify(results)

@bp.route('/models/', methods=['POST'])
def process_models_request():
    available_models = ["Transformer", "Relative-Transformer", "BiLSTM", "TreeLSTM"]
    # result = json.dumps(available_models)
    return jsonify(available_models)

@bp.route('/databases/', methods=['POST'])
def process_databases_request():
    available_database_names = ['not available']
    # current_app.logger.info(available_database_names)
    return jsonify(available_database_names)
