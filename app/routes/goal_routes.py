from flask import Blueprint,request,abort,make_response
from app.models.goal import Goal
from ..db import db
from .route_utilities import validate_model

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()

    if not "title" in request_body:
        return ({"details": "Invalid data"},400)
    else:
        new_goal = Goal.from_dict(request_body)

    
        db.session.add(new_goal)
        db.session.commit()

        response = {"goal" : new_goal.to_dict()}
        return response,201
    
@bp.get("")
def get_all_goals():
    
    query = db.select(Goal)
    sorted_title = request.args.get("sort")
    if sorted_title == "desc":
        query = query.order_by(Goal.title.desc())
    else:
        query = query.order_by(Goal.title.asc())
                            
    goals = db.session.scalars(query)

    goals_response =([goal.to_dict() for goal in goals],200)
    
    return goals_response

@bp.get("/<goal_id>")
def get_single_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal" : goal.to_dict()}

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    new_goal = Goal.from_dict(request_body)
   
    db.session.commit()
    return {"goal" : goal.to_dict()}

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()



    return {

        "details": 'Goal 1 "Build a habit of going outside daily" successfully deleted'
    }