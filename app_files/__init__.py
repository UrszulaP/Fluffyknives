from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = "546fd15ec3802ecc4ec4789d324cc647"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

from app_files import routes
# import w tym miejscu, aby uniknąć circular import