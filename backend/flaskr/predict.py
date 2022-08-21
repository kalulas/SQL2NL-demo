from flask import (Blueprint, request, redirect, url_for)

bp = Blueprint('predict', __name__, url_prefix="/predict")

@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'GET':
        return redirect('/../') # to home page
    
    if request.method == 'POST':
        return "<p>predict function WIP</p>" #TODO
