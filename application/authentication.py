from flask_login import LoginManager
from application import app, db
from bson import ObjectId
from .models import User

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = 'auth_bp.login'
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(email):
    user = db.users.find_one_or_404({"email": email})
    if user:
        user = User(user['_id'], user['name'], user['email'], user['password'], user['role'])
        return user
    return None