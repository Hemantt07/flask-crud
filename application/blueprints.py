from application import app
from application.routes.auth import auth_bp
from application.routes.blogs import blog_bp


app.register_blueprint(blog_bp, url_prefix='/blogs')
app.register_blueprint(auth_bp, url_prefix='/')