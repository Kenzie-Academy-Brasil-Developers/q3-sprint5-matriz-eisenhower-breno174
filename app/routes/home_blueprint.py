from flask import Blueprint

from app.controllers import get_home

bp_home = Blueprint("home", __name__, url_prefix="/")

bp_home.get('')(get_home)
