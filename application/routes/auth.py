from flask import Blueprint, request, url_for, render_template, flash, redirect
from application import db
from datetime import datetime
from werkzeug.utils import secure_filename
from bson import ObjectId
from ..models import User
from application import app
import os
from ..authentication import load_user
from flask_login import login_required, login_user, logout_user, current_user
from application import bcrypt
from ..mail_config import send_registration_email

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        if db.users.find_one({"email": email}):
            flash('Email already registered', 'error')
            return redirect(request.url)
        
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        if confirmPassword != password:
            flash('Passwords do not match!', 'danger')
            return redirect(request.url)

        hashed_password = bcrypt.generate_password_hash(password)
        try:
            new_user = db.users.insert_one({
                "name": name,
                "email": email,
                "password": hashed_password,
                "is_active": True,
                "role": 'User',
                "date_created": datetime.utcnow()
            })
            send_registration_email(email, name=name)

            flash("You have registered successfully!", "success")
            return redirect(url_for('auth_bp.login'))
        except Exception as e:
            flash("An error occurred while creating the user: {}".format(str(e)), "error")
            return redirect(url_for('auth_bp.register'))

    return render_template('users/register.html')

@auth_bp.route("/delete_user/<id>")
def delete_user(id):
    db.users.find_one_and_delete({"_id": ObjectId(id)})
    flash("Blog successfully deleted", "danger")
    return redirect( url_for( 'auth_bp.index' ) )


@auth_bp.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = db.users.find_one({"email": email}) 
        if user:
            stored_password = user['password']
            
            if bcrypt.check_password_hash(stored_password, password):
                new_user = User( user['_id'], user['name'], user['email'], user['password'], user['role'] )
                login_user(new_user, remember=True)
                return redirect(url_for('auth_bp.dashboard'))
            else:
                flash("Incorrect Password, try again!", "error")
                return redirect(request.url)
        else:
            flash("User not found", "danger")
            return redirect(request.url)

    return render_template('users/login.html')

@auth_bp.route('dashboard')
@login_required
def dashboard():
    return render_template( 'users/profile.html' )

@auth_bp.route('logout')
@login_required
def logout():
    logout_user()
    return redirect( url_for( 'auth_bp.login' ) ) 

@auth_bp.route('edit-profile',  methods = ['POST', 'GET'])
@login_required
def edit_profile():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        image = request.files.get('profile-picture')
        if image is None or image.filename == '':
            image_path = current_user.profile_image
        else:
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image_path = filename
        user_id = ObjectId(current_user.id)

        db.users.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": {
            "name": name,
            "email": email,
            "profile_image": image_path,
        }})

        load_user(email=email)

        flash("Your profile has been updated", "success")
        return redirect(request.url)

    else:
        return render_template( 'users/edit-profile.html' )