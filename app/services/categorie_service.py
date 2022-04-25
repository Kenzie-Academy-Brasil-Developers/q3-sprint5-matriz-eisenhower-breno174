from flask import request
from app.models.categories import CategoriesModel
from app.models.tasks import TasksModel
from app.configs.database import db
from sqlalchemy.orm import Session
from ipdb import set_trace

from app.services.exceptions import KeysNotAccepted, KeysTypeError, MandatoryKeyMissing


TRUSTED_KEYS = [
    "name", "description"
]


def serialized_categorie(payload: TasksModel):
    response = {
        "id": payload.id,
        "name": payload.name,
        "description": payload.description
    }
    return response

def check_keys():
    data = request.get_json()
    keys = data.keys()
    for key in keys:
        if key not in TRUSTED_KEYS:
            raise KeysNotAccepted
    values = data.values()
    for value in values:
        if type(value) != str:
            raise KeysTypeError
    try:
        data['name']
    except:
        raise MandatoryKeyMissing
