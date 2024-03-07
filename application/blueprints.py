from application import app
from application.routes.users import user_bp
from application.routes.blogs import blog_bp


app.register_blueprint(blog_bp, url_prefix='/blogs')
app.register_blueprint(user_bp, url_prefix='/users')