from flask import Flask, render_template, json, jsonify
from flask_pymongo import PyMongo
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = "b2945762b9d4b39e190b1c0a38099f7ced53624a"
app.config["MONGO_URI"] = 'mongodb://localhost:27017/Flask'
upload_dir = os.getcwd() + '/application/static/uploads'
app.config['UPLOAD_FOLDER'] = upload_dir

mongo = PyMongo(app)
db = mongo.db

from application import blueprints

@app.route('/')
def index():
    return render_template('layout.html')
