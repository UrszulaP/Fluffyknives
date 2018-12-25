from flask import redirect, url_for, render_template, request
from app_files import app, db, bcrypt
from app_files.forms import RegistrationForm, LoginForm, UpdateAccountForm, OrderStatusForm, NewItemForm
from app_files.db_models import User, Item, Order
from flask_login import login_user, current_user, logout_user, login_required
import secrets # secrets for images names hashing - to make it not repeted
import os # os to get file extention name
from PIL import Image # Pillow - to change images size

#------------------------------------ MAIN PAGE -----------------------------------------#

@app.route('/')
def root():
	itemsList = Item.query.all()
	return render_template('main.html', itemsList=itemsList)


#------------------------------------ LOGIN PAGE ----------------------------------------#

@app.route('/login', methods=['GET', 'POST'])
def login():
	# checks if the current user is logged in - built-in function from flask_login
	if current_user.is_authenticated:
		return redirect(url_for('root'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		# built-in function from bcrypt, comparing password from the db with password from the form
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			# built-in function from flask-login, remember argue takes value from the form checkbox "Remember Me"
			login_user(user, remember=form.remember.data)
			# takes 'next' argue from querystring and after login redirecs at once for requested page,
			# (where login was required), not to root
			# in login.html needs to be <form action = ""> not to delete 'next' parameter
			# get() instead of [] - if 'next' parameter doesn`t exist, it will return None instead of throwing an error
			nextPage = request.args.get('next')
			return redirect(nextPage) if nextPage else redirect(url_for('root'))
		else:
			return render_template('login_failed.html')
	return render_template('login.html', form=form)


#----------------------------------- LOGOUT PAGE ----------------------------------------#

@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('root'))


#-------------------------------- REGISTRATION PAGE -------------------------------------#

@app.route('/register', methods=['GET', 'POST'])
def register():
	# checks if the current user is logged in - built-in function from flask_login
	if current_user.is_authenticated:
		return redirect(url_for('root'))
	form = RegistrationForm()
	if form.validate_on_submit():
		hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		# next user_id is created automatically
		user = User(username=form.username.data, email=form.email.data, password=hashedPassword)
		db.session.add(user)
		db.session.commit()
		return render_template('register_ok.html')
	return render_template('register.html', form=form)


#---------------------------------- ACCOUNT PAGE ----------------------------------------#

# profile upload function
def savePicture(formPicture):
	# generates random hash (8 characters)
	randomHex = secrets.token_hex(8)
	# separates file name and file extention
	fName, fileExtension = os.path.splitext(formPicture.filename) # _ - sign of unused value
	pictureFilename = randomHex + fileExtension
	# defines path to save picture
	picturePath = os.path.join(app.root_path, 'static/images/profile_pictures', pictureFilename)
	# changes the image size while saving
	outputSize = (125, 125)
	resizedPicture = Image.open(formPicture)
	resizedPicture.thumbnail(outputSize)
	# saves picture to the folder
	resizedPicture.save(picturePath)
	# returns file name to save it in the database
	return pictureFilename

@app.route('/account', methods=['GET', 'POST'])
# decorator from flask_login
@login_required
def account():
	# no access for admin
	if current_user.isAdmin:
		return redirect(url_for('root'))
	form = UpdateAccountForm()
	# user data changing
	if form.validate_on_submit():
		# if, because adding a profile picture is not required
		if form.picture.data:
			# saving picture file to /profile_pictures
			pictureFile = savePicture(form.picture.data)
			# deleting an old profile picture
			if current_user.imageFile != 'defaultpp.jpg':
				oldPicturePath = os.path.join(app.root_path, 'static/images/profile_pictures', current_user.imageFile)
				os.remove(oldPicturePath)
			current_user.imageFile = pictureFile
			
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.adress = form.adress.data
		current_user.phone = form.phone.data
		db.session.commit()
		# while rendering the same page, redirect must me used -
		# if render_template is used, after refreshing the page, POST will be resend (appears a question about resending the form)
		return render_template('updated.html')
	# fills form fields with the current values
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.adress.data = current_user.adress
		form.phone.data = current_user.phone
	# determines the profile picture path
	imageFile = url_for('static', filename='images/profile_pictures/' + current_user.imageFile)
	return render_template('account.html', form=form, imageFile=imageFile)


#--------------------------------- USER ORDERS PAGE -------------------------------------#

@app.route('/cart', methods=['GET', 'POST'])
# dekorator z flask_login
@login_required
def cart():
	# no access for admin, no reaction for POST after click on "Zamów" by admin
	if current_user.isAdmin:
		return redirect(url_for('root'))
	if request.method == 'POST':
		# takes itemID from main.html
		orderedItemID = int(request.form['orderedItemID'])
		# makes an order object, adds it to the database
		order = Order(itemID=orderedItemID, userID=current_user.id)
		db.session.add(order)
		db.session.commit()
	# queries about orders of logged user
	# query(Order) - acces to Order; query(Order, Item), to make access to Item as well, which is joint by join clause
	ordersList = db.session.query(Order, Item).filter(Order.userID==current_user.id).join(Item, Order.itemID==Item.id)
	return render_template('cart.html', ordersList=ordersList)


#------------------------------- SHOP MANAGEMENT PAGE -----------------------------------#

# item picture upload function
def saveItemPicture(formPicture):
	# generates random hash (8 characters)
	randomHex = secrets.token_hex(8)
	# separates file name and file extention
	fName, fileExtension = os.path.splitext(formPicture.filename) # _ - sign of unused value
	pictureFilename = randomHex + fileExtension
	# defines path to save picture
	picturePath = os.path.join(app.root_path, 'static/images/shop', pictureFilename)
	# changes the image size while saving
	outputSize = (700, 700)
	resizedPicture = Image.open(formPicture)
	resizedPicture.thumbnail(outputSize)
	# saves picture to the folder
	resizedPicture.save(picturePath)
	# returns file name to save it in the database
	return pictureFilename

@app.route('/shopmanagement', methods=['GET', 'POST'])
# decorator from flask_login
@login_required
def shopmanagement():
	if current_user.isAdmin:
		# deletes item from the database by form from itmes table
		# try - because there are 2 forms in template, handles an error while adding an item
		try:
			# takes itemID from shopmanagement.html
			deletedItemID = int(request.form['deletedItemID'])
			# queries about item object from database
			deletedItem = Item.query.filter_by(id=deletedItemID).first()
			# deletes item picture
			picturePath = os.path.join(app.root_path, 'static/images/shop', deletedItem.itemImage)
			os.remove(picturePath)
			# deletes an item from the database
			db.session.delete(deletedItem)
			db.session.commit()
			# while rendering the same page, redirect must me used -
			# if render_template is used, after refreshing the page, POST will be resend (appears a question about resending the form)
			# and validation of the second form will apear
			return redirect(url_for('shopmanagement'))
		except:
			# adds a new item
			# it may be in except, form will always be loaded
			# name different from 'form' must be used, because 'form' is already used in template to delete items
			formNewItem = NewItemForm()
			if formNewItem.validate_on_submit():
				# saves image file to /shop, saves changed name of the picture
				newItemImage = saveItemPicture(formNewItem.itemImage.data)
				# adds item to the database
				item = Item(itemName=formNewItem.itemName.data, 
					itemMainDescription=formNewItem.itemMainDescription.data, 
					itemPointsDescription=formNewItem.itemPointsDescription.data, 
					itemImage=newItemImage, 
					itemPrice=formNewItem.itemPrice.data)
				db.session.add(item)
				db.session.commit()
				# while rendering the same page, redirect must me used -
			# if render_template is used, after refreshing the page, POST will be resend (appears a question about resending the form)
			# and the form will stay filled
				return redirect(url_for('shopmanagement'))
		# list of all of the items in shop to the template
		itemsList = Item.query.all()
		return render_template('shopmanagement.html', itemsList=itemsList, form=formNewItem)
	else:
		return redirect(url_for('root'))


#--------------------------------- ALL ORDERS PAGE --------------------------------------#

@app.route('/orders', methods=['GET', 'POST'])
# decorator from flask_login
@login_required
def orders():
	if current_user.isAdmin:
		form = OrderStatusForm()
		# changes order status in case of POST
		if form.validate_on_submit():
			# takes order number, which change refers to
			orderID = form.orderID.data
			# queries about order object by its id
			order = db.session.query(Order).filter(Order.id==orderID).first()
			# changes order status in the database
			order.status = form.status.data
			db.session.commit()
		# queries about all orders
		# query(Order) - queries Order; query(Order, Item), to make access to Item and User as well, which are joint by join clause
		ordersList = db.session.query(Order, Item, User).join(Item, Order.itemID==Item.id).join(User, Order.userID==User.id).all()
		return render_template('orders.html', ordersList=ordersList, form=form)
	else:
		return redirect(url_for('root'))