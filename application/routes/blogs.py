from flask import Blueprint, request, url_for, render_template, flash, redirect
from application import db
from werkzeug.utils import secure_filename
from datetime import datetime
from bson import ObjectId
import os
from application import app
from flask_login import current_user, login_required
blog_bp = Blueprint('blog_bp', __name__)

@blog_bp.route('/')
def index():
    blogs = list(db.blogs.find({}))

    for blog in blogs:
        if '_id' in blog:
            blog['_id'] = str(blog['_id'])
            user = db.users.find_one({'_id': ObjectId(blog['created_by'])})
            blog['created_by'] = user['name']
            blog['user_image'] = user['profile_image'] if 'profile_image' in user else ''
    return render_template('blogs/guest-view.html', blogs=blogs)
    
@blog_bp.route('/own')
def my_blogs():
    if current_user.is_authenticated:
        blogs = list(db.blogs.find({"created_by": current_user.id}))

        for blog in blogs:
            if '_id' in blog:
                blog['_id'] = str(blog['_id'])
        return render_template('blogs/index.html', blogs=blogs)
    return redirect( 'auth_bp.login' )

@blog_bp.route("/view/<id>")
def view_blog(id):
    blog = db.blogs.find_one_or_404({"_id": ObjectId(id)})
    blog['_id'] = str(blog['_id'])
    return render_template( 'blogs/view.html', blog=blog )
    

@blog_bp.route('/create', methods=['POST', 'GET'])
@login_required
def create():
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
            db.blogs.insert_one({
                "name": title,
                "description": description,
                "image": image_path,
                "date_created": datetime.utcnow(),
                "created_by": current_user.id
            })
            flash("Blog successfully created", "success")
        except Exception as e:
            flash("An error occurred while creating the blog", "error")
            return redirect( url_for( 'blog_bp.index' ) )
    else:
        pass
    return render_template( 'blogs/create.html' )

@blog_bp.route("/delete_blog/<id>")
@login_required
def delete_blog(id):
    db.blogs.find_one_and_delete({"_id": ObjectId(id)})
    flash("Blog successfully deleted", "danger")
    return redirect( url_for( 'blog_bp.index' ) )


@blog_bp.route("/update_blog/<id>", methods = ['POST', 'GET'])
@login_required
def update_blog(id):
    existing_blog = db.blogs.find_one({"_id": ObjectId(id)})
    if existing_blog['created_by'] != ObjectId(current_user.id):
        flash('You can edit your own post only', 'error')
        return redirect( url_for('blog_bp.index') )
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
                if existing_blog:
                    image_path = existing_blog.get('image')

        db.blogs.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": title,
            "description": description,
            "image": image_path,
        }})

        flash("Blog successfully updated", "success")
        return redirect(request.url)
    else:
        blog = db.blogs.find_one_or_404({"_id": ObjectId(id)})
        blog['_id'] = str(blog['_id'])

    return render_template( 'blogs/edit.html', blog=blog )