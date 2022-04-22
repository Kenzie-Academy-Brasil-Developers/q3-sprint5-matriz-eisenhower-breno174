from flask import jsonify, request
from sqlalchemy.orm import Query, Session
from app.configs.database import db
from app.controllers.home_controller import initial_populate
from app.models.categories import CategoriesModel
from app.models.eisenhower import EisenhowerModel
from app.models.tasks import TasksModel
from app.services.tasks_service import check_categories
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
    
    new_task = check_categories(data)
    # print(new_task.__dict__)
    # trash = new_task.__dict__.pop['_sa_instance_state']
    serialaized = {
        # "id": "",
        "name": new_task.name,
        "description": new_task.description,
        "duration": new_task.duration,
        "classification": query.type,
        "categories": new_task.categories
    }

    return jsonify(serialaized), 200


def patch_task(id):
    ...


def delete_task(id):
    ...
