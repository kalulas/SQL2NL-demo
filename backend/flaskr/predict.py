from flask import Blueprint, request, redirect

bp = Blueprint('predict', __name__, url_prefix="/predict")

@bp.route('/', methods=('GET', 'POST'))
def predict_index():
    if request.method == 'GET':
        return redirect('/../') # to home page
    
    if request.method == 'POST':
        return "<p>predict function WIP</p>" #TODO
