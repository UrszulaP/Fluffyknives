from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

app.config['SECRET_KEY'] = "546fd15ec3802ecc4ec4789d324cc647"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt()

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from app_files import routes  # import here to avoid circular import error
