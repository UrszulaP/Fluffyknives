from app_files import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'User'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='defaultpp.jpg')
    adress = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Item(db.Model):
    __tablename__ = 'Item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    short_description = db.Column(db.String(30))
    detailed_description = db.Column(db.String(200))
    image = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Item('{self.name}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.ForeignKey('Item.id'))
    user_id = db.Column(db.ForeignKey('User.id'))
    status = db.Column(db.String, nullable=False, default='W trakcie realizacji')
    item = db.relationship('Item', backref="user_associations")
    user = db.relationship('User', backref="item_associations")

    def __repr__(self):
        return f"Order('{self.id}', {self.item_id}', '{self.user_id}')"
