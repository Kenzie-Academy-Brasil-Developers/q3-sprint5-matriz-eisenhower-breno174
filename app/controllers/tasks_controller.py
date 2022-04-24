from bdb import set_trace
from flask import jsonify, request
from sqlalchemy.orm import Query, Session
from sqlalchemy.exc import IntegrityError
from app.configs.database import db
from app.controllers.home_controller import initial_populate
from app.models.categories import CategoriesModel
from app.models.eisenhower import EisenhowerModel
from app.models.tasks import TasksModel
from app.services.tasks_service import check_categories, register_task
from app.services.eisenhower import defining_eisenhower


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
        "classification": query.type,
        "categories": serilized_categories
    }

    return jsonify(serialaized), 200


def patch_task(id):
    ...


def delete_task(id):
    ...
