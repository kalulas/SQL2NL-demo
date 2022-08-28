from flask import Blueprint, request, redirect

bp = Blueprint('predict', __name__, url_prefix="/predict")

@bp.route('/', methods=('GET', 'POST'))
def predict_index():
    if request.method == 'GET':
        return redirect('/../') # to home page
    
    if request.method == 'POST':
        selected_models = request.json['selected']
        input_sql = request.json['sql'].upper()
        result = ""
        for model in selected_models:
            result = result + f"[{model}] {input_sql}\n"

        return result #TODO
