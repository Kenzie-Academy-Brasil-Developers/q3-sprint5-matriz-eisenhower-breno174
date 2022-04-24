from flask import request
from app.models.categories import CategoriesModel
from app.models.tasks import TasksModel
from app.configs.database import db
from sqlalchemy.orm import Session
from ipdb import set_trace

from app.services.exceptions import KeysNotAccepted, KeysTypeError, MandatoryKeyMissing


TRUSTED_KEYS = [
    "name", "description", "duration", "importance", "urgency", "categories"
]

def register_task(payload):
    session: Session = db.session
    data_categories = payload.pop('categories')
    all_categories = session.query(CategoriesModel).all()
    
    names = [categ.name for categ in all_categories]
    new_task = TasksModel(**payload)

    not_record = [name for name in data_categories if name not in names]
    for record in not_record:
        new_categ = CategoriesModel(name=record)
        session.add(new_categ)
        session.commit()

    for x in data_categories:
        new_task.categories.append(session.query(CategoriesModel).filter_by(name = x).first())

    session.add(new_task)
    session.commit()
    return new_task


def check_categories(payload):
    data_categories = payload['categories']
    for name in data_categories:
        if type(name) != str:
            raise TypeError


def serialized_task(payload: TasksModel):
    response = {
        "id": payload.id,
        "name": payload.name,
        "description": payload.description,
        "duration": payload.duration,
        "classifcation": payload.eisenhower.type
    }
    return response

def check_keys():
    data = request.get_json()
    keys = data.keys()
    for key in keys:
        if key not in TRUSTED_KEYS:
            raise KeysNotAccepted
    try:
        data['name']
    except:
        raise MandatoryKeyMissing
    if type(data['name']) != str:
        raise KeysTypeError
    if "description" in list(data.keys()):
        if type(data['description']) != str:
            raise KeysTypeError
    check_categories(data)
