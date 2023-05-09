from flask import Blueprint, abort, jsonify, make_response, request
from app import db
from app.models.task import Task
import datetime
from dotenv import load_dotenv
import requests
import os

load_dotenv()


task_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

def validate_model(model, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"msg": f"Task {model_id} invalid"}, 400))
    
    task = Task.query.get(model_id)

    if not task:
        abort(make_response({"msg": f"Task {model_id} not found"}, 404))

    return task

@task_bp.route("", methods=["POST"])
def add_task():
    request_body = request.get_json()
    try:
        new_task = Task.from_dict(request_body)
        # (
        #     title = request_body["title"],
        #     description = request_body["description"],
        #     completed_at = None
        # )
    except KeyError:
        return {
            "details": "Invalid data"
        }, 400

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@task_bp.route("", methods=["GET"])
def get_task():
    response = []

    title_query = request.args.get("title")
    sort_query = request.args.get("sort")

    if title_query:
        tasks = Task.query.filter_by(title=title_query)
    elif sort_query == "asc":
        tasks = Task.query.order_by(Task.title)
    elif sort_query == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.all()
    
    #refactor to do list comprehension
    for task in tasks: 
        response.append(task.to_dict())

    
    print(tasks)

    return (jsonify(response), 200)

@task_bp.route("/<task_id>", methods=["GET"])
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return {"task":task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["PUT"])
def update_task(task_id):
    task = validate_model(Task,task_id)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit()

    return {"task":task.to_dict()}, 200

@task_bp.route("/<task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {'details': f'Task {task.task_id} "{task.title}" successfully deleted'}, 200

@task_bp.route("/<task_id>/mark_complete", methods=["PATCH"])
def mark_complete(task_id):
    task = validate_model(Task,task_id)

    task.completed_at = datetime.datetime.now()

    db.session.commit()

    data_bot = {
        "token": os.environ.get("SLACKBOT_TOKEN_API"),
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(url="https://slack.com/api/chat.postMessage", data=data_bot)

    return {"task": task.to_dict()}, 200

@task_bp.route("/<task_id>/mark_incomplete", methods=["PATCH"])
def mark_incomplete(task_id):
    task = validate_model(Task,task_id)

    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200
