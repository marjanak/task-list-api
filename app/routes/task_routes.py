from flask import Blueprint,request,abort,make_response,Response
from app.models.task import Task
from ..db import db

tasks_bp = Blueprint("tasks_bp",__name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    if not "title" in request_body:
        return ({"details": "Invalid data"},400)
    elif not "description" in request_body:
        return ({"details": "Invalid data"},400)
    else:
        title = request_body["title"]
        description = request_body["description"]
        completed_at = None
    
        new_task = Task(title=title, description=description, completed_at=None)
    
        db.session.add(new_task)
        db.session.commit()

        response = {"task" : new_task.to_dict()}

        return response,201

@tasks_bp.get("")
def get_all_tasks():
    
    query = db.select(Task)
    sorted_title = request.args.get("sort")
    if sorted_title == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.title.asc())
                            
    tasks = db.session.scalars(query)

    tasks_response =([task.to_dict() for task in tasks],200)
    
    return tasks_response

    
@tasks_bp.get("/<task_id>")
def get_single_task(task_id):
    task = validate_task(task_id)

    return {"task" : task.to_dict()}

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = None
    
    db.session.commit()
    return {"task" : task.to_dict()}

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return {

        "details": 'Task 1 "Go on my daily walk 🏞" successfully deleted'
    }
#Response(status=204, mimetype="application/json")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message":f"Task {task_id} is invalid, 400"}))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
  
    if not task:
        abort(make_response({"message":f"Task {task_id} is not found, 404"},404))
       
    return task 

    
             
             
