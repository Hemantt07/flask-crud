from flask import Flask, render_template, request, jsonify
from flask_pymongo import PyMongo
import os
from bson import ObjectId
from flask_bcrypt import Bcrypt
from .background_tasks.tasks import add_numbers

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config["SECRET_KEY"] = "b2945762b9d4b39e190b1c0a38099f7ced53624a"
app.config["MONGO_URI"] = 'mongodb://localhost:27017/Flask'
# app.config["MONGO_URI"] = 'mongodb+srv://hemantdhiman:i4l2yR5orzBCEvjV@flask.3mooitq.mongodb.net/?retryWrites=true&w=majority'
upload_dir = os.getcwd() + '/application/static/uploads'

app.config['UPLOAD_FOLDER'] = upload_dir

mongo = PyMongo(app)
db = mongo.db

@app.route('/')
def index():
    blogs = list(db.blogs.find({}))

    for blog in blogs:
        if '_id' in blog:
            blog['_id'] = str(blog['_id'])
            user = db.users.find_one({'_id': ObjectId(blog['created_by'])})
            blog['created_by'] = user['name']
            blog['user_image'] = user['profile_image'] if 'profile_image' in user else ''
    return render_template('blogs/guest-view.html', blogs=blogs)


from application import blueprints
from application import mail_config
from application import authentication
from .text_generator import generate_text_withai 
from .error_templates import server_error, not_found_error

