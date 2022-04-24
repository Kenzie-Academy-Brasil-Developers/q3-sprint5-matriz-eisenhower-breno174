from http import HTTPStatus
from flask import jsonify
from sqlalchemy.orm.session import Session
from ipdb import set_trace
from app.configs.database import db
from app.models.categories import CategoriesModel
from app.models.eisenhower import EisenhowerModel
from app.services.tasks_service import serialized_task


def get_home():
    session: Session = db.session
    all_categories = session.query(CategoriesModel).all()
    if all_categories == []:
        return {"message": "whitout content"}, HTTPStatus.NO_CONTENT

    serialized = []
    for categorie in all_categories:
        task = [serialized_task(task) for task in categorie.tasks]
        categorie = {
            "id": categorie.id,
            "name": categorie.name,
            "description": categorie.description,
            "tasks": task
        }
        serialized.append(categorie)

    return jsonify(serialized), 200


def initial_populate():
    session: Session = db.session
    eisenhower_table = session.query(EisenhowerModel).all()

    if eisenhower_table == []:
        eisen1 = EisenhowerModel(type="Dot It First")
        eisen2 = EisenhowerModel(type="Delegate It")
        eisen3 = EisenhowerModel(type="Schedule It")
        eisen4 = EisenhowerModel(type="Delete It")

        session.add(eisen1)
        session.add(eisen2)
        session.add(eisen3)
        session.add(eisen4)
        session.commit()
