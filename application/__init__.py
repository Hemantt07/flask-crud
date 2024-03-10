from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
import os
from flask_bcrypt import Bcrypt
from .background_tasks.tasks import add_numbers

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config["SECRET_KEY"] = "b2945762b9d4b39e190b1c0a38099f7ced53624a"
app.config["MONGO_URI"] = 'mongodb://localhost:27017/Flask'
upload_dir = os.getcwd() + '/application/static/uploads'

app.config['UPLOAD_FOLDER'] = upload_dir

mongo = PyMongo(app)
db = mongo.db

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    x = data.get('x')
    y = data.get('y')
    result = add_numbers.delay(x, y)
    return jsonify({'task_id': result.id}), 202

@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    result = add_numbers.AsyncResult(task_id)
    if result.ready():
        return jsonify({'result': result.get()}), 200
    else:
        return jsonify({'status': 'pending'}), 202


from application import blueprints
from application import mail_config
from application import authentication
from .text_generator import generate_text_withai 
from .error_templates import server_error, not_found_error

@app.route('/')
def index():
    return render_template('layout.html')
