from http import HTTPStatus
from ipdb import set_trace

from app.configs.database import db
from app.controllers.home_controller import initial_populate
from app.models.categories import CategoriesModel
from app.models.eisenhower import EisenhowerModel
from app.models.tasks import TasksModel
from app.models.tasks import TasksModel
from app.services.eisenhower import defining_eisenhower
from app.services.exceptions import KeysNotAccepted, KeysTypeError, MandatoryKeyMissing
from app.services.tasks_service import check_categories, check_keys, register_task
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query, Session


def create_task():
    session: Session = db.session
    initial_populate()
    data = request.get_json()
    try:
        check_keys()
        check_categories(data)
        eisenhower = defining_eisenhower(data)
    except TypeError:
        return {"error": "categories types not allowed, must be strings"}, HTTPStatus.BAD_REQUEST
    except MandatoryKeyMissing:
        return {"error": "the key 'name' has to be in the request"}, HTTPStatus.BAD_REQUEST
    except KeysNotAccepted:
        return {
            "error": "bad keys",
            "keys accepted": ["name", "description", "duration", "importance", "urgency", "categories"],
            "received keys": list(data.keys())
            }, HTTPStatus.BAD_REQUEST
    except KeysTypeError:
        return {"error": "name and description types must be strings"}, HTTPStatus.BAD_REQUEST
    except AttributeError:
        return {"msg": "urgency and importance types must be integer"}, HTTPStatus.BAD_REQUEST

    if not eisenhower:
        return {
            "msg": {
                    "valid_options": {
                    "importance": [1, 2],
                    "urgency": [1, 2]
                    },
                    "recieved_options": {
                    "importance": data['importance'],
                    "urgency": data['urgency']
                    }
                }
            }, HTTPStatus.BAD_REQUEST

    query: Query = (session.query(EisenhowerModel).filter_by(type=eisenhower).first())
    eisenhower_id = query.id
    data['eisenhower_id'] = eisenhower_id
    try:
        new_task = register_task(data)
    except IntegrityError as err:
        if type(err.orig).__name__ == "UniqueViolation":
            return {"error": "Unique Violation"}, HTTPStatus.CONFLICT

    serilized_categories = [categorie.name for categorie in new_task.categories]
    serialaized = {
        "id": new_task.id,
        "name": new_task.name,
        "description": new_task.description,
        "duration": new_task.duration,
        "classification": new_task.eisenhower.type,
        "categories": serilized_categories
    }

    return jsonify(serialaized), HTTPStatus.CREATED


def patch_task(id):
    data = request.get_json()
    session: Session = db.session
    task = session.query(TasksModel).filter(TasksModel.id == id).first()
    
    if not task:
        return {"error": "id not found"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(task, key, value)
    serilized = {
        "id": task.id,
        "name": task.name,
        "description": task.description
    }

    session.commit()

    return jsonify(serilized), HTTPStatus.OK


def delete_task(id):
    session: Session = db.session
    task = session.query(TasksModel).get(id)
    if not task:
        return {"error": "id not found"}, HTTPStatus.NOT_FOUND

    session.delete(task)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
