from http import HTTPStatus
from flask import jsonify
from sqlalchemy.orm.session import Session
from app.configs.database import db
from app.models.categories import CategoriesModel
from app.models.eisenhower import EisenhowerModel


def get_home():
    session: Session = db.session
    all_categories = session.query(CategoriesModel).all()
    if all_categories == []:
        return {"message": "whitout content"}, HTTPStatus.NO_CONTENT

    response = [categorie.__dict__ for categorie in all_categories]
    seriealized = [seri.pop('_sa_instance_state') for seri in response]

    return jsonify(response), 200


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
