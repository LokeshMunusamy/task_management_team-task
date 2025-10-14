# validation.py

import re
from functools import wraps
from flask import request, jsonify
from datetime import datetime

email_pattern = r'^[a-zA-Z0-9._]+@[a-zA-Z0-9]+\.[a-z]{2,}$'
password_pattern = r'^[A-Za-z0-9]{8,}$'

# signup validation
def validate_signup(func):
    @wraps(func)
    def validation(*args, **kwargs):
        data = request.get_json()

        if not data['name'].strip():
            return jsonify({"status": "error", "message": "Name cannot be empty"}), 400

        if not re.fullmatch(email_pattern, data['email']):
            return jsonify({"status": "error", "message": "Invalid email format"}), 400

        if not re.fullmatch(password_pattern, data['password']):
            return jsonify({"status": "error", "message":"Password must be at least 8 characters with letters and numbers"}), 400

        return func(*args, **kwargs)
    return validation


# login validation
def validate_login(func):
    @wraps(func)
    def validation(*args, **kwargs):
        data = request.get_json()

        if not re.fullmatch(email_pattern, data['email']):
            return jsonify({"status": "error", "message": "Invalid email format"}), 400

        if not re.fullmatch(password_pattern, data['password']):
            return jsonify({"status": "error", "message":"Password must be at least 8 characters with letters and numbers"}), 400

        return func(*args, **kwargs)
    return validation

# add tasks
def create_task(funs):
    @wraps(funs)
    def validation(*args, **kwargs):
        data = request.get_json()

        title = data.get("title")
        description = data.get("description")
        status = data.get("status")
        priority = data.get("priority")
        due_date = data.get("due_date")
        # user_id = data.get("user_id")

        if not title:
            return jsonify({"error": "Title is required"}), 400

        if not description:
            return jsonify({"error": "Description is required"}), 400

        if not status or status not in ["pending", "complete"]:
            
            return jsonify({"error": "Status is required only allow pending or complete"}), 400

        if not priority or priority not in ["low", "medium", "high"]:
            return jsonify({"error": "Priority is required only allow low, medium and high"}), 400

        if not due_date:
            return jsonify({"error": "Due date is required"}), 400

        # if not user_id:
        #     return jsonify({"error": "User ID is required"}), 400

        return funs(*args, **kwargs)
    return validation


def update_validation(func):
    @wraps(func)
    def validations(*args, **kwargs):
        data = request.get_json()

        required_fields = ["title", "description", "status", "priority", "due_date"]
        missing = [field for field in required_fields if field not in data or not str(data[field]).strip()]

        if missing:
            return jsonify({"error": f"Missing or empty fields: {', '.join(missing)}"}), 400

        allowed_status = ["pending", "in progress", "complete"]
        if data["status"].lower() not in allowed_status:
            return jsonify({"error": f"Invalid status. Allowed: {', '.join(allowed_status)}"}), 400

        allowed_priority = ["low", "medium", "high"]
        if data["priority"].lower() not in allowed_priority:
            return jsonify({"error": f"Invalid priority. Allowed: {', '.join(allowed_priority)}"}), 400

        try:
            datetime.strptime(data["due_date"], "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        return func(*args, **kwargs)
    return validations
