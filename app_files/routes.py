from flask import redirect, url_for, render_template, request
from app_files import app, db, bcrypt
from app_files.forms import RegistrationForm, LoginForm, UpdateAccountForm, OrderStatusForm, NewItemForm
from app_files.db_models import User, Item, Order
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image

@app.route('/')
def root():
    itemsList = Item.query.all()
    return render_template('main.html', itemsList=itemsList)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user and bcrypt.check_password_hash(user.password, 
                                                form.password.data)):
            login_user(user, remember=form.remember.data)
            nextPage = request.args.get('next')
            return redirect(nextPage) if nextPage else redirect(url_for('root')) # !!!!!!!!!!!!!!!!!!!!!!!!
        else:
            return render_template('login_failed.html')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('root'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('root'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashedPassword = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, 
                    email=form.email.data, 
                    password=hashedPassword)
        db.session.add(user)
        db.session.commit()
        return render_template('register_ok.html')
    return render_template('register.html', form=form)


def saveUserPicture(formPicture):
    randomHex = secrets.token_hex(8)
    fileName, fileExtension = os.path.splitext(formPicture.filename)
    pictureFilename = randomHex + fileExtension
    picturePath = os.path.join(app.root_path, 
                               'static/images/profile_pictures', 
                               pictureFilename)
    outputSize = (125, 125)
    resizedPicture = Image.open(formPicture)
    resizedPicture.thumbnail(outputSize)
    resizedPicture.save(picturePath)
    return pictureFilename

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if current_user.isAdmin:
        return redirect(url_for('root'))

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            pictureFile = saveUserPicture(form.picture.data)
            if current_user.imageFile != 'defaultpp.jpg':
                oldPicturePath = os.path.join(app.root_path, 
                                              'static/images/profile_pictures', 
                                              current_user.imageFile)
                os.remove(oldPicturePath)
            current_user.imageFile = pictureFile
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.adress = form.adress.data
        current_user.phone = form.phone.data
        db.session.commit()
        return render_template('updated.html')

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.adress.data = current_user.adress
        form.phone.data = current_user.phone

    imageFile = url_for('static', filename='images/profile_pictures/' 
                        + current_user.imageFile)
    return render_template('account.html', form=form, imageFile=imageFile)


@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if current_user.isAdmin:
        return redirect(url_for('root'))
    # if posted form from main.html
    if request.method == 'POST':
        orderedItemID = int(request.form['orderedItemID'])
        order = Order(itemID=orderedItemID, userID=current_user.id)
        db.session.add(order)
        db.session.commit()
    userOrdersList = db.session.query(Order, Item).filter(Order.userID==current_user.id).join(Item, Order.itemID==Item.id)
    return render_template('cart.html', userOrdersList=userOrdersList)


def saveItemPicture(formPicture):
    randomHex = secrets.token_hex(8)
    fileName, fileExtension = os.path.splitext(formPicture.filename)
    pictureFilename = randomHex + fileExtension
    picturePath = os.path.join(app.root_path, 
                               'static/images/shop', 
                               pictureFilename)
    outputSize = (700, 700)
    resizedPicture = Image.open(formPicture)
    resizedPicture.thumbnail(outputSize)
    resizedPicture.save(picturePath)
    return pictureFilename

@app.route('/shopmanagement', methods=['GET', 'POST'])
@login_required
def shopmanagement():
    if current_user.isAdmin:
        # try - because there are 2 forms in template, 
        # handles an error while adding an item
        try:
            # deletes item from the database by form from itmes table
            deletedItemID = int(request.form['deletedItemID'])
            deletedItem = Item.query.filter_by(id=deletedItemID).first()
            picturePath = os.path.join(app.root_path, 'static/images/shop', 
                                       deletedItem.itemImage)
            os.remove(picturePath)
            db.session.delete(deletedItem)
            db.session.commit()
            return redirect(url_for('shopmanagement'))
        except:
            # adds a new item
            # it may be in except, form will always be loaded
            # name different from 'form' must be used, 
            # because 'form' is already used in template to delete items         ??????????????????
            formNewItem = NewItemForm()
            if formNewItem.validate_on_submit():
                newItemImage = saveItemPicture(formNewItem.itemImage.data)
                item = Item(itemName=formNewItem.itemName.data, 
                            itemMainDescription=formNewItem.itemMainDescription.data, 
                            itemPointsDescription=formNewItem.itemPointsDescription.data, 
                            itemImage=newItemImage, 
                            itemPrice=formNewItem.itemPrice.data)
                db.session.add(item)
                db.session.commit()
                return redirect(url_for('shopmanagement'))
        itemsList = Item.query.all()
        return render_template('shopmanagement.html', 
                               itemsList=itemsList, form=formNewItem)
    else:
        return redirect(url_for('root'))


@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    if current_user.isAdmin:
        form = OrderStatusForm()
        if form.validate_on_submit():
            orderID = form.orderID.data
            order = db.session.query(Order).filter(Order.id==orderID).first()
            order.status = form.status.data
            db.session.commit()
        ordersList = db.session.query(Order, Item, User).join(Item, Order.itemID==Item.id).join(User, Order.userID==User.id).all()
        return render_template('orders.html', 
                               ordersList=ordersList, form=form)
    else:
        return redirect(url_for('root'))