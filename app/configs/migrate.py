from flask import Flask
from flask_migrate import Migrate

mg = Migrate()

def init_app(app: Flask):
    # import models
    mg.init_app(app, app.db, compare_type=True)
