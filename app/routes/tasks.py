
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, Blueprint
from app.models import db, TaskModel
from app.schemas import TaskSchema
from marshmallow import ValidationError
from redis import Redis
from rq import Queue
import os
from app.jobs import send_due_date_notification

tasks_blp = Blueprint('tasks', __name__)

schema = TaskSchema() 

redis_client = Redis.from_url(os.getenv('REDIS_URL', 'redis://localhost:6379'))
notif_queue = Queue(connection=redis_client)

@tasks_blp.route('/tasks', methods=['GET'])
def get_tasks():
    query = TaskModel.query.all()
    
    completed = request.args.get('completed')
    if completed is not None:
        completed = completed.lower() == 'true'
        query = TaskModel.query.filter_by(completed=completed)
    return jsonify({"tasks": [q.to_dict() for q in query]}), 200

@tasks_blp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = TaskModel.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200

@tasks_blp.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    task = TaskModel(**data)
    db.session.add(task)
    db.session.commit()

    notification_queued = False
    if task.due_date:
        current = datetime.utcnow()
        if current < task.due_date <= current+timedelta(hours=24): 
            notif_queue.enqueue(send_due_date_notification, task.title)
            notification_queued = True


    return jsonify({"task": task.to_dict(), "notification_queued": notification_queued}), 201

@tasks_blp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = TaskModel.query.get_or_404(task_id)
    try:
        data = schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    
    updated_at = datetime.utcnow()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    task.due_date = data.get('due_date', task.due_date)
    task.category_id = data.get('category_id', task.category_id)
    task.updated_at = updated_at

    db.session.commit()
    return jsonify({"task": task.to_dict()}), 200

@tasks_blp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = TaskModel.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"}), 200