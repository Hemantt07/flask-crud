from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["SECRET_KEY"] = "b2945762b9d4b39e190b1c0a38099f7ced53624a"
app.config["MONGO_URI"] = "mongodb+srv://hemantdhiman:i4l2yR5orzBCEvjV@flask.3mooitq.mongodb.net/?retryWrites=true&w=majority"

# mongodb client
mongodb_client = PyMongo(app)
mongo_database = mongodb_client.db

try:
    # Test database connection
    mongodb_client.cx.server_info()
    print("Connected to MongoDB")
except Exception as e:
    print("Error connecting to MongoDB:", e)

from application import routes
