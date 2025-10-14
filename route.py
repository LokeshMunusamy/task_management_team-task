# route.py

from flask import request, jsonify, session
from init import app
from validation import validate_signup, validate_login, create_task, update_validation
from database_operations import Create_operations
from datetime import datetime
import jwt

SECRET_KEY = "user_allow"

def login_id(token):
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    return decoded.get('user_id')

@app.route('/signup', methods=['POST'])
@validate_signup
def signup():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    result = Create_operations.signup_method(name, email, password)
    return jsonify(result), 200 if result["status"] == "success" else 400


@app.route('/login', methods=['GET'])
@validate_login
def login():
    global login_id
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    token = session.get("token")

    if not token:

        result = Create_operations.login_method(email, password)
        # decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # id = decoded.get('user_id')
        # login_id = id
        # print(login_id)
        return jsonify(result), 200 if result["status"] == "success" else 400
    else:
        return jsonify({"status": "error", "message": "already user login"})


@app.route('/add_task', methods=['POST'])
@create_task
def assign_task():
    # global login_id
    data = request.get_json()

    title = data.get("title")
    description = data.get("description")
    status = data.get("status")
    priority = data.get("priority")
    due_date_str = data.get("due_date")
    user_id = login_id(session.get("token"))

    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    result = Create_operations.new_task(
        title, description, status, priority, due_date, user_id
    )
    return jsonify(result), 200 if result.get("status") == "success" else 400



@app.route('/update_task/<task_id>', methods=['PUT'])
@update_validation
def update_task(task_id):
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")
    priority = data.get("priority")
    due_date_str = data.get("due_date")
    user_id = login_id(session.get("token"))
    
    try:
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    result = Create_operations.update_task(task_id, title, description, status, priority, due_date, user_id)
    return jsonify(result), result.get("status_code", 200)



@app.route('/delete_task/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    id = login_id(session.get("token"))
    
    result = Create_operations.delete_task(task_id, id)
    return jsonify(result), result.get("status_code", 200)


@app.route("/filter/<field>", methods=['GET'])
def filter_task(field):
    id = login_id(session.get("token"))
    result = Create_operations.filter_task(field, id)
    return jsonify(result)


@app.route("/sorted_data", methods=['GET'])
def sort_method():
    id = login_id(session.get("token"))
    result = Create_operations.sorted_data(id)
    return jsonify(result)



@app.route("/profile", methods=["GET"])
def update_user():
    id = login_id(session.get("token"))
    print("route", id)
    result = Create_operations.get_profile(id)
    return jsonify(result)



@app.route("/get_token", methods=['GET'])
def get_token():
    # id = login_id(session.get("token"))
    token = session.get("token")
    if token:
        # decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        # # print(decoded, id)
        return jsonify({"status": "success", "token": token})
    return jsonify({"status": "error", "message": "No session token found"}), 400

@app.route("/remove_session")
def remove_session():
    session.clear()
    return jsonify({"status": "success"})


if __name__ == '__main__':
    app.run(debug=True)

