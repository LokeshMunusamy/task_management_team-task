# database_operattion.py

from bson import ObjectId
from flask import session
from init import Database
import jwt
from pymongo import ASCENDING, DESCENDING
from datetime import datetime, timedelta, timezone

SECRET_KEY = "user_allow"

class Create_operations:

    @staticmethod
    def signup_method(name, mail, password):
        db = Database.conn("users")
        check = db.find_one({'email': mail})
        if check:
            return {"status": "error", "message": "Mail ID already exists"}

        db.insert_one({
            "name": name,
            "email": mail,
            "password": password,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        })
        return {"status": "success", "message": "User registered successfully"}


    @staticmethod
    def login_method(mail, password):
        db = Database.conn("users")

        user = db.find_one({"email": mail, "password": password})
        if not user:
            return {"status": "error", "message": "Invalid credentials"}

        token = jwt.encode(
            {
                "user_id": str(user["_id"]),
                "email": user["email"],
                "exp": datetime.now(timezone.utc) + timedelta(minutes = 30)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        session.permanent = True
        session["token"] = token
        return {"status": "success", "message": "Login successful", "token": token}

    @staticmethod
    def new_task(title, description, status, priority, due_date, user_id):
        print(user_id)
        db = Database.conn("task_maintain")
        check_id = Database.conn("users").find_one({"_id": ObjectId(user_id)})

        if not check_id:
            return {"status": "error", "message": "user not found"}

        db.insert_one({
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
            "due_date": due_date,
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        })
        return {"status": "success", "message": "Task created successfully"}
    
    @staticmethod
    def update_task(task_id, title, description, status, priority, due_date, user_id):
        db = Database.conn("task_maintain")

        check = db.find_one({"_id": ObjectId(task_id),"user_id": user_id})
        if not check:
            return {"status": "error", "message": "Task not found", "status_code": 404}

        update_data = {
            "title": title,
            "description": description,
            "status": status,
            "priority": priority,
            "user_id": user_id,
            "due_date": due_date,
            "updated_at": datetime.now(timezone.utc)
        }

        update_data = {k: v for k, v in update_data.items() if v is not None}

        result = db.update_one({"_id": ObjectId(task_id)}, {"$set": update_data})

        if result.modified_count == 0:
            return {"status": "error", "message": "No changes made", "status_code": 400}

        return {"status": "success", "message": "Task updated successfully", "status_code": 200}
    

    @staticmethod
    def delete_task(task_id, login_id):
        db = Database.conn("task_maintain")
        try:
            result = db.delete_one({"_id": ObjectId(task_id), "user_id": login_id})

            if result.deleted_count == 0:
                return {"status": "error", "message": "Task not found", "status_code": 404}

            return {"status": "success", "message": "Task deleted successfully"}
        except:
            return {"status": "error", "message": "Unauthorized user", "status_code": 401}

    @staticmethod
    def filter_task(field, login_id):
        db = Database.conn("task_maintain")

        if field in ["low", "medium", "high"]:
            result = list(db.find({"priority": field, "user_id": login_id}))
            for val in result:
                val['_id'] = str(val['_id'])
            return result

        
        elif field in ["pending", "complete"]:
            result = list(db.find({"status": field, "user_id": login_id}))
            for val in result:
                val['_id'] = str(val['_id'])
            return result


        else:
            return {
                "status": "error",
                "message": "Invalid field or value",
                "status_code": 401
            }
        
    # @staticmethod
    # def sorted_data(user_id):
    #     db = Database.conn("task_maintain")
    #     user = db.find({"_id": ObjectId(user_id)}).sort("due_date", ASCENDING)
    #     return user

    @staticmethod
    def sorted_data(user_id):
        db = Database.conn("task_maintain")

        tasks = list(db.find({"user_id": user_id}).sort("due_date", ASCENDING))

        for task in tasks:
            task["_id"] = str(task["_id"])

        return tasks

        
    @staticmethod
    def get_profile(user_id):
            print(user_id)
        
            db = Database.conn("users")
            user = db.find_one({"_id": ObjectId(user_id)})
            
            if not user:
                return {"status": "error", "message": "User not found", "status_code": 404}
        
            return {
                "status": "success",
                "data": {
                    "profile": {
                        "id": str(user["_id"]),
                        "name": user.get("name"),
                        "email": user.get("email"),
                        "created_time": user.get("created_time"),
                        "updated_time": user.get("updated_time")
                    }
                }
            }
    
    