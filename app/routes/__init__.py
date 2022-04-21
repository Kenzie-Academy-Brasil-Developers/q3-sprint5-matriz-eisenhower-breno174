from flask import Flask, Blueprint
from app.routes.categories_blueprint import bp_categories
from app.routes.home_blueprint import bp_home
from app.routes.tasks_blueprint import bp_tasks

bp_main = Blueprint("matriz", __name__)

def init_app(app: Flask):
    bp_main.register_blueprint(bp_categories)
    bp_main.register_blueprint(bp_tasks)
    bp_main.register_blueprint(bp_home)

    app.register_blueprint(bp_main)
