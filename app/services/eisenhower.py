from flask import request
from app.models.tasks import TasksModel
from app.services.exceptions import ScopeError


def defining_eisenhower(payload):
    importance = payload['importance']
    urgency = payload['urgency']
    if not type(importance) == int or not type(urgency) == int:
        raise AttributeError
    if importance == 1 and urgency == 1:
        return "Dot It First"
    if importance == 1 and urgency == 2:
        return "Delegate It"
    if importance == 2 and urgency == 1:
        return "Schedule It"
    if importance == 2 and urgency == 2:
        return "Delete It"


def patch_eisenhower(payload: TasksModel):
    data = request.get_json()
    try:
        payload.importance = data['importance']
    except:
        pass
    try:
        payload.urgency = data['urgency']
    except:
        pass
    if type(payload.importance) != int:
        raise AttributeError
    if type(payload.urgency) != int:
        raise AttributeError

    if payload.importance > 2 or payload.importance < 1:
        raise ScopeError
    if payload.urgency > 2 or payload.urgency < 1:
        raise ScopeError

    if payload.importance == 1 and payload.urgency == 1:
        payload.eisenhower.type = "Dot It First"
    if payload.importance == 1 and payload.urgency == 2:
        payload.eisenhower.type = "Delegate It"
    if payload.importance == 2 and payload.urgency == 1:
        payload.eisenhower.type = "Schedule It"
    if payload.importance == 2 and payload.urgency == 2:
        payload.eisenhower.type = "Delete It"
