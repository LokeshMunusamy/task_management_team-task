# init.py

from flask import Flask
from flask_session import Session
from datetime import timedelta
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "supersecretkey"

app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.permanent_session_lifetime = timedelta(minutes=30)

Session(app)  

class Database:
    @staticmethod
    def conn(table_name):
        connect = MongoClient("mongodb://localhost:27017/")
        db = connect["task_management"]
        return db[table_name]
