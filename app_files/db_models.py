from app_files import db, login_manager
from flask_login import UserMixin
# UserMixin class contains functions required by flask_login
# (is_authenticated, is_active, is_anonymous, get_id)
# UserMixin needs to be added to User class inheritance

# function needed to indicate user_id for login_manager
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))

#------------------------------ DATABASE SCHEME ----------------------------------#

class User(db.Model, UserMixin):
	__tablename__ = 'User' # name needs to be given to make relationship working

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	password = db.Column(db.String(60), nullable=False)
	imageFile = db.Column(db.String(20), nullable=False, default='defaultpp.jpg')
	adress = db.Column(db.String(200))
	phone = db.Column(db.String(20))
	isAdmin = db.Column(db.Boolean, default=False)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"



class Item(db.Model):
	__tablename__ = 'Item' # name needs to be given to make relationship working

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
	itemID = db.Column(db.ForeignKey('Item.id'))  # nullable=Flase causes an error when a new row is added in my db editor
	userID = db.Column(db.ForeignKey('User.id'))  # as above
	status = db.Column(db.String, nullable = False, default='W trakcie realizacji')

	item = db.relationship('Item', backref="user_associations")
	user = db.relationship('User', backref="item_associations")

	def __repr__(self):
		return f"Order('{self.id}', {self.itemID}', '{self.userID}')"
	