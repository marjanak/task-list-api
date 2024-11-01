from flask import Blueprint,request,Response
from app.models.task import Task
from ..db import db

tasks_bp = Blueprint("tasks_bp",__name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body["completed_at"]
    

    new_task = Task(title=title, description=description, completed_at=completed_at)
    
    db.session.add(new_task)
    db.session.commit()

    response = new_task.to_dict()
    return response,201

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task).order_by(Task.id)
    tasks = db.session.scalars(query)

    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response

