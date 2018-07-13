from app_files import db, login_manager
from flask_login import UserMixin
# klasa UserMixin zawiera wymagane przez rozszerzenie flask_login funkcje
# is_authenticated, is_active, is_anonymous, get_id
# trzeba je dodać do dziedziczenia klas bazy danych

# ------------------------------SCHEMAT BAZY DANYCH----------------------------------#

@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

# ------------------------------SCHEMAT BAZY DANYCH----------------------------------#

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
