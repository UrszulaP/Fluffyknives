from flask import redirect, url_for, render_template, request
from app_files import app, db, bcrypt
from app_files.forms import RegistrationForm, LoginForm, UpdateAccountForm, \
    OrderStatusForm, NewItemForm
from app_files.db_models import User, Item, Order
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image


@app.route('/')
def root():
    items = Item.query.all()
    return render_template('main.html', items=items)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root'))

    login_form = LoginForm()

    if request.method == 'POST' and login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and password_matches(user.password, login_form.password.data):
            login_user(user, remember=login_form.remember.data)
            return redirect_after_login()
        else:
            return render_template('login_failed.html')
    else:
        return render_template('login.html', form=login_form)


def password_matches(entered_pass, actual_pass):
    return bcrypt.check_password_hash(entered_pass, actual_pass)


def redirect_after_login():
    next_page = request.args.get('next')
    if next_page:
        return redirect(next_page)
    else:
        return redirect(url_for('root'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('root'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('root'))

    user_form = RegistrationForm()

    if request.method == 'POST' and user_form.validate_on_submit():
        save_user(user_form)
        return render_template('register_ok.html')
    else:
        return render_template('register.html', form=user_form)


def save_user(user_form):
    hashed_password = (bcrypt.generate_password_hash(user_form.password.data)
                       .decode('utf-8'))
    user = User(
        username=user_form.username.data,
        email=user_form.email.data,
        password=hashed_password)
    db.session.add(user)
    db.session.commit()


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if current_user.is_admin:
        return redirect(url_for('root'))

    user_form = UpdateAccountForm()
    if request.method == 'POST' and user_form.validate_on_submit():  # impossible to send PATCH request from HTML template
        update_user(user_form)
        return render_template('updated.html')
    
    elif request.method == 'GET':
        set_user_form_data(user_form)

    image_file = url_for(
        'static',
        filename='images/profile_pictures/' + current_user.image_file)
    return render_template('account.html', form=user_form, image_file=image_file)


def update_user(user_form):
    if user_form.picture.data:
        picture_file = save_picture(user_form.picture.data, '/profile_pictures', 125)
        if current_user.image_file != 'defaultpp.jpg':
            delete_picture(current_user.image_file, '/profile_pictures')
        current_user.image_file = picture_file
    current_user.username = user_form.username.data
    current_user.email = user_form.email.data
    current_user.adress = user_form.adress.data
    current_user.phone = user_form.phone.data
    db.session.commit()


def save_picture(picture_file, path, size):
    random_hex = secrets.token_hex(8)
    file_name, file_extension = os.path.splitext(picture_file.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(
        app.root_path,
        'static/images' + path,
        picture_filename)
    output_size = (size, size)
    resized_picture = Image.open(picture_file)
    resized_picture.thumbnail(output_size)
    resized_picture.save(picture_path)
    return picture_filename


def delete_picture(filename, path):
    old_picture_path = os.path.join(
        app.root_path, 'static/images' + path, filename)
    os.remove(old_picture_path)


def set_user_form_data(user_form):
    user_form.username.data = current_user.username
    user_form.email.data = current_user.email
    user_form.adress.data = current_user.adress
    user_form.phone.data = current_user.phone


@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if current_user.is_admin:
        return redirect(url_for('root'))

    if request.method == 'POST':  # comes from main.html
        save_order()

    user_orders = (db.session.query(Order, Item)
                   .filter(Order.user_id == current_user.id)
                   .join(Item, Order.item_id == Item.id))
    return render_template('cart.html', user_orders=user_orders)


def save_order():
    ordered_item_id = int(request.form['ordered_item_id'])
    order = Order(item_id=ordered_item_id, user_id=current_user.id)
    db.session.add(order)
    db.session.commit()


@app.route('/shopmanagement', methods=['GET', 'POST'])
@login_required
def shopmanagement():
    if not current_user.is_admin:
        return redirect(url_for('root'))

    item_form = NewItemForm()
    if request.method == 'POST' and item_form.validate_on_submit():
        save_item(item_form)
        return redirect(url_for('shopmanagement'))

    items = Item.query.all()
    return render_template('shopmanagement.html', items=items, form=item_form)


def save_item(item_form):
    new_item_image = save_picture(item_form.image.data, '/shop', 700)
    item = Item(
        name=item_form.name.data,
        short_description=item_form.short_description.data,
        detailed_description=item_form.detailed_description.data,
        image=new_item_image,
        price=item_form.price.data)
    db.session.add(item)
    db.session.commit()


@app.route('/items/delete/<item_id>', methods=['POST'])  # impossible to send DELETE request from HTML template
@login_required
def delete_item(item_id):
    if not current_user.is_admin:
        return redirect(url_for('root'))

    item_to_delete = Item.query.filter_by(id=item_id).first()
    delete_picture(item_to_delete.image, '/shop')
    db.session.delete(item_to_delete)
    db.session.commit()
    return redirect(url_for('shopmanagement'))


@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders_management():
    if not current_user.is_admin:
        return redirect(url_for('root'))

    order_status_form = OrderStatusForm()
    if request.method == 'POST' and order_status_form.validate_on_submit():  # impossible to send PATCH request from HTML template
        update_order_status(order_status_form)

    orders = (db.session.query(Order, Item, User)
              .join(Item, Order.item_id == Item.id)
              .join(User, Order.user_id == User.id).all())
    return render_template('orders.html', orders=orders, form=order_status_form)


def update_order_status(order_status_form):
    order_id = order_status_form.order_id.data
    order = db.session.query(Order).filter(
        Order.id == order_id).first()
    order.status = order_status_form.status.data
    db.session.commit()
