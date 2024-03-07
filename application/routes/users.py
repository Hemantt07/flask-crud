from flask import Blueprint, request, url_for, render_template, flash, redirect
from application import db
from werkzeug.utils import secure_filename
from datetime import datetime
from bson import ObjectId
import os
from application import app

user_bp = Blueprint('user_bp', __name__)

# @user_bp.route('/')
# def index():
#     users = list(db.users.find({}))
#     for user in users:
#         if '_id' in user:
#             user['_id'] = str(user['_id'])

#     return render_template('users/index.html', users=users)

@user_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        title = request.form.get('name')
        description = request.form.get('description')
        if 'image' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        image = request.files['image']
        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = filename

        try:
            db.users.insert_one({
                "name": title,
                "description": description,
                "image": image_path,
                "date_created": datetime.utcnow()
            })
            flash("Blog successfully created", "success")
        except Exception as e:
            flash("An error occurred while creating the user", "error")
            return redirect( url_for( 'user_bp.index' ) )
    else:
        pass
    return render_template( 'users/register.html' )

@user_bp.route("/delete_user/<id>")
def delete_user(id):
    db.users.find_one_and_delete({"_id": ObjectId(id)})
    flash("Blog successfully deleted", "danger")
    return redirect( url_for( 'user_bp.index' ) )


@user_bp.route("/update_user/<id>", methods = ['POST', 'GET'])
def update_user(id):
    if request.method == "POST":
        title = request.form.get('name')
        description = request.form.get('description')
        image_path = None 
        if 'image' in request.files:
            image = request.files['image']
            if image.filename:
                filename = secure_filename(image.filename)
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_path = filename
            else:
                existing_user = db.users.find_one({"_id": ObjectId(id)})
                if existing_user:
                    image_path = existing_user.get('image')

        db.users.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": title,
            "description": description,
            "image": image_path,
        }})

        flash("Blog successfully updated", "success")
        return redirect(request.url)
    else:
        user = db.users.find_one_or_404({"_id": ObjectId(id)})
        user['_id'] = str(user['_id'])

    return render_template( 'users/edit.html', user=user )