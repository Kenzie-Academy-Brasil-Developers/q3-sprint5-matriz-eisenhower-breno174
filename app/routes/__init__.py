from flask import Flask, Blueprint

bp_main = Blueprint("matriz", __name__, url_prefix='categories')

def init_app(app: Flask):
    
    app.register_blueprint(bp_main)
