from flask import Blueprint, render_template

bp = Blueprint('homepage', __name__, url_prefix="/")

@bp.route('/')
def homepage_index():
    return render_template('index.html')
    # return '<p>index.html WIP</p><img src="https://tse1-mm.cn.bing.net/th/id/OIP-C.tsfohpXnAjmqwuAEBBhn8AHaEf?pid=ImgDet&rs=1"/>'