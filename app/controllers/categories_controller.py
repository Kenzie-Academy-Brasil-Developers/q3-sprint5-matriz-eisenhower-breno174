from http import HTTPStatus
from flask import jsonify, request
from sqlalchemy.orm.session import Session
from app.models.categories import CategoriesModel
from app.configs.database import db


def create_categorie():
    data = request.get_json()
    session: Session = db.session

    categorie = CategoriesModel(**data)

    session.add(categorie)
    session.commit()

    return jsonify({
        "name": categorie.name,
        "description": categorie.description,
        "tasks": categorie.tasks
    }), HTTPStatus.CREATED


def patch_categorie(id):
    data = request.get_json()
    session: Session = db.session
    categorie = session.query(CategoriesModel).filter(CategoriesModel.id == id).first()
    
    if not categorie:
        return {"error": "id not found"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(categorie, key, value)
    serilized = {
        "id": categorie.id,
        "name": categorie.name,
        "description": categorie.description
    }

    session.commit()

    return jsonify(serilized), HTTPStatus.OK


def delete_categorie(id):
    session: Session = db.session
    categorie = session.query(CategoriesModel).get(id)
    if not categorie:
        return {"error": "id not found"}, HTTPStatus.NOT_FOUND

    session.delete(categorie)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
