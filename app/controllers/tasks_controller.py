from http import HTTPStatus
from ipdb import set_trace

from app.configs.database import db
from app.controllers.home_controller import initial_populate
from app.models.categories import CategoriesModel
from app.models.eisenhower import EisenhowerModel
from app.models.tasks import TasksModel
from app.models.tasks import TasksModel
from app.services.eisenhower import defining_eisenhower
from app.services.tasks_service import check_categories, register_task
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Query, Session


def create_task():
    session: Session = db.session
    initial_populate()
    data = request.get_json()
    try:
        eisenhower = defining_eisenhower(data)
    except TypeError:
        return "", 401

    query: Query = (session.query(EisenhowerModel).filter_by(type=eisenhower).first())
    eisenhower_id = query.id
    data['eisenhower_id'] = eisenhower_id
    try:
        check_categories(data)
    except TypeError:
        return {"error": "categories types not allowed, must be strings"}, 401
    try:
        new_task = register_task(data)
    except IntegrityError:
        return {"error": "task already registred"}, 401

    serilized_categories = [categorie.name for categorie in new_task.categories]
    serialaized = {
        "id": new_task.id,
        "name": new_task.name,
        "description": new_task.description,
        "duration": new_task.duration,
        "classification": new_task.eisenhower.type,
        "categories": serilized_categories
    }

    return jsonify(serialaized), 201


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
