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
	__tablename__ = 'User'	# trzeba nadać nazwę, aby relationship działał

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='defaultpp.jpg')
	adress = db.Column(db.String(200))
	phone = db.Column(db.String(20))
	isAdmin = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"



class Item(db.Model):
	__tablename__ = 'Item'	# trzeba nadać nazwę, aby relationship działał

	id = db.Column(db.Integer, primary_key=True)
	itemName = db.Column(db.String(30), unique=True, nullable=False)
	itemMainDescription = db.Column(db.String(30))
	itemPointsDescription = db.Column(db.String(200))
	itemImage = db.Column(db.String(30), nullable=False)
	itemPrice = db.Column(db.Float, nullable=False)

	def __repr__(self):
		return f"Item('{self.itemName}')"



class Order(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	itemID = db.Column(db.ForeignKey('Item.id'))	# nullable=Flase powoduje błąd przy dodawaniu nowego wiersza
	userID = db.Column(db.ForeignKey('User.id'))	# j.w.
	status = db.Column(db.String, nullable = False, default='W trakcie realizacji')

	item = db.relationship('Item', backref="user_associations")
	user = db.relationship('User', backref="item_associations")

	def __repr__(self):
		return f"Order('{self.id}', {self.itemID}', '{self.userID}')"
	