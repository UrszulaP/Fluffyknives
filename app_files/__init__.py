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
# ustala, gdzie ma być przekierowany użytkownik niezalogowany,
# przy wykorzystaniu @login_required (z flask-login) dla danego widoku
# tu - do url_for('login')
login_manager.login_view = 'login'

# import w tym miejscu, aby uniknąć circular import
from app_files import routes
