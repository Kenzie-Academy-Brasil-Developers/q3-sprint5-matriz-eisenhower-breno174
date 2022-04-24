from app.models.tasks import TasksModel


def defining_eisenhower(payload):
    importance = payload['importance']
    urgency = payload['urgency']
    if not type(importance) == int or not type(urgency) == int:
        raise TypeError
    if importance == 1 and urgency == 1:
        return "Dot It First"
    if importance == 1 and urgency == 2:
        return "Delegate It"
    if importance == 2 and urgency == 1:
        return "Schedule It"
    if importance == 2 and urgency == 2:
        return "Delete It"
    return "Delete It"
