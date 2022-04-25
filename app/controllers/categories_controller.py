from http import HTTPStatus
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from app.models.categories import CategoriesModel
from app.configs.database import db
from app.services.categorie_service import check_keys as keys_categories
from app.services.exceptions import KeysNotAccepted, KeysTypeError, MandatoryKeyMissing


def create_categorie():
    data = request.get_json()
    session: Session = db.session
    try:
        keys_categories()
    except KeysNotAccepted:
        return {
            "error": "bad keys",
            "keys accepted": ["name", "description"],
            "received keys": list(data.keys())
            }, HTTPStatus.BAD_REQUEST
    except MandatoryKeyMissing:
        return {"error": "the key 'name' has to be in the request"}, HTTPStatus.BAD_REQUEST
    except KeysTypeError:
        return {"error": "name and description types must be strings"}, HTTPStatus.BAD_REQUEST

    categorie = CategoriesModel(**data)
    try:
        session.add(categorie)
        session.commit()
    except IntegrityError as err:
        if type(err.orig).__name__ == "UniqueViolation":
            return {"error": "Unique Violation"}, HTTPStatus.CONFLICT

    return jsonify({
        "name": categorie.name,
        "description": categorie.description,
        "tasks": categorie.tasks
    }), HTTPStatus.CREATED


def patch_categorie(id):
    data = request.get_json()
    session: Session = db.session
    try:
        ...
    except:
        ...
    categorie = session.query(CategoriesModel).filter(CategoriesModel.id == id).first()
    
    if not categorie:
        return {"error": "categorie not found"}, HTTPStatus.NOT_FOUND

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
        return {"error": "categorie not found"}, HTTPStatus.NOT_FOUND

    session.delete(categorie)
    session.commit()

    return "", HTTPStatus.NO_CONTENT
