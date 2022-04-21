from flask import Blueprint

from app.controllers import create_task, delete_task, patch_task

bp_tasks = Blueprint("tasks", __name__, url_prefix="/tasks")

bp_tasks.post('')(create_task)
bp_tasks.patch('<id>')(patch_task)
bp_tasks.delete('<id>')(delete_task)
