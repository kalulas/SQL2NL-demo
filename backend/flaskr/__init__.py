import os

from flask import Flask

def create_app(test_config=None):
    """ 
    reference: https://dormousehole.readthedocs.io/en/latest/tutorial/factory.html
    """
    
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev', # replace this in production
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    
    # this is for database
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def _():
        return '<p>index.html WIP</p><img src="https://tse1-mm.cn.bing.net/th/id/OIP-C.tsfohpXnAjmqwuAEBBhn8AHaEf?pid=ImgDet&rs=1"/>'

    from . import predict
    app.register_blueprint(predict.bp)

    return app