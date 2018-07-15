from app_files import db, login_manager
from flask_login import UserMixin
# klasa UserMixin zawiera wymagane przez rozszerzenie flask_login funkcje
# is_authenticated, is_active, is_anonymous, get_id
# trzeba je dodać do dziedziczenia klas bazy danych

# funkcja potrzebna do wskazania user_id do login_manager
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

class Item(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	itemName = db.Column(db.String(30), unique=True, nullable=False)
	itemMainDescription = db.Column(db.String(30))
	itemPointsDescription = db.Column(db.String(200))
	itemImage = db.Column(db.String(30))
	itemPrice = db.Column(db.Float, nullable=False)

	def __repr__(self):
		return f"Item('{self.itemName}')"