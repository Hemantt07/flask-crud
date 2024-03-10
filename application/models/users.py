from application import db
from datetime import datetime


users = db.users.find({})

def find_user(email):
    for user in users:
        if user.email == email:
            return user
    return None

class User:
    def __init__(self, id, name, email, password, role):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.role = role
    
    def register(self):
        user =  db.users.insert_one({
                "name": self.name,
                "email": self.email,
                "password": self.hashed_password,
                "is_active": True,
                "date_created": datetime.utcnow()
            })
        
        return user
        

    def get_user(self, email):
        user = db.users.find_one_or_404({'email': email})
        return user

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False