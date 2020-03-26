from datetime import datetime
from Flask_Dashboard import db,login_manager  # from __init__.py
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):         # user_id stored in session var
    return User.query.get(int(user_id))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(20),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(60),nullable=False)
    #posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class Doctor(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    doctor = db.Column(db.String(20),unique=True,nullable=False)
    drugName = db.Column(db.String(120),unique=True,nullable=False)
    status = db.Column(db.String(60),nullable=False)
    dosage = db.Column(db.String(60),nullable=False)
    frequency = db.Column(db.String(60),nullable=False)
    #posts = db.relationship('Post',backref='author',lazy=True)

    def __repr__(self):
        return f"Doctor('{self.Doctor}','{self.DrugName}')"

