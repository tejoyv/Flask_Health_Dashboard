from flask import Flask
from flask_bcrypt import Bcrypt 
from flask_sqlalchemy import SQLAlchemy 
from flask_login import LoginManager 

app=Flask(__name__)
app.config['SECRET_KEY'] = '93de1f13b99630eb23d480f16f31f5cc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from Flask_Dashboard import routes
