from application import app
from flask import render_template, request, redirect, flash, url_for

from bson import ObjectId

from .forms import BlogForm
from application import mongo_database
from datetime import datetime


@app.route("/")
def get_blogs():
    blogs = list(mongo_database.blogs.find().sort("date_created", -1))
    for blog in blogs:
        blog["_id"] = str(blog["_id"])
        blog["date_created"] = blog["date_created"].strftime("%b %d %Y %H:%M:%S")
    return render_template("view_blogs.html", blogs=blogs)

    

@app.route("/add_blog", methods = ['POST', 'GET'])
def add_blog():
    if request.method == "POST":
        form = BlogForm(request.form)
        blog_name = form.title.data
        blog_description = form.description.data
        blog_image = form.image.data

        mongo_database.blogs.insert_one({
            "name": blog_name,
            "description": blog_description,
            "image": blog_image,
            "date_created": datetime.utcnow()
        })
        flash("Blog successfully added", "success")
        return redirect("/")
    else:
        form = BlogForm()
    return render_template("blogs/add_blog.html", form = form)


@app.route("/delete_blog/<id>")
def delete_blog(id):
    mongo_database.blogs.find_one_and_delete({"_id": ObjectId(id)})
    flash("Blog successfully deleted", "success")
    return redirect("/")


@app.route("/update_blog/<id>", methods = ['POST', 'GET'])
def update_blog(id):
    if request.method == "POST":
        form = BlogForm(request.form)
        blog_name = form.name.data
        blog_description = form.description.data
        completed = form.completed.data

        mongo_database.blogs.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": blog_name,
            "description": blog_description,
            "completed": completed,
            "date_created": datetime.utcnow()
        }})
        flash("Blog successfully updated", "success")
        return redirect("/")
    else:
        form = BlogForm()

        blog = mongo_database.blogs.find_one_or_404({"_id": ObjectId(id)})
        print(blog)
        form.name.data = blog.get("name", None)
        form.description.data = blog.get("description", None)
        form.completed.data = blog.get("completd", None)

    return render_template("add_blog.html", form = form)