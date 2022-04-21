from flask import Blueprint

from app.controllers import create_categorie, delete_categorie, patch_categorie

bp_categories = Blueprint("categories", __name__, url_prefix="/categories")

bp_categories.post('')(create_categorie)
bp_categories.patch('<id>')(patch_categorie)
bp_categories.delete('<id>')(delete_categorie)
