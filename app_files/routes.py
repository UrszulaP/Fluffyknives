from flask import redirect, url_for, render_template, request
from app_files import app, db, bcrypt
from app_files.forms import RegistrationForm, LoginForm, UpdateAccountForm, \
    OrderStatusForm, NewItemForm
from app_files.db_models import User, Item, Order
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
from PIL import Image


def save_user_picture(form_picture):
    random_hex = secrets.token_hex(8)
    file_name, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(
        app.root_path,
        'static/images/profile_pictures',
        picture_filename)
    output_size = (125, 125)
    resized_picture = Image.open(form_picture)
    resized_picture.thumbnail(output_size)
    resized_picture.save(picture_path)
    return picture_filename


def delete_old_picture(user):
    if user.image_file != 'defaultpp.jpg':
        old_picture_path = os.path.join(
            app.root_path,
            'static/images/profile_pictures',
            user.image_file)
        os.remove(old_picture_path)


def save_item_picture(form_picture):
    random_hex = secrets.token_hex(8)
    file_name, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(
        app.root_path,
        'static/images/shop',
        picture_filename)
    output_size = (700, 700)
    resized_picture = Image.open(form_picture)
    resized_picture.thumbnail(output_size)
    resized_picture.save(picture_path)
    return picture_filename


@app.route('/')
def root():
    items_list = Item.query.all()
    return render_template('main.html', items_list=items_list)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('root'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if (user and bcrypt.check_password_hash(
                user.password,
                form.password.data)):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('root'))
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
        hashed_password = (bcrypt.generate_password_hash(form.password.data)
                           .decode('utf-8'))
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return render_template('register_ok.html')
    return render_template('register.html', form=form)


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if current_user.is_admin:
        return redirect(url_for('root'))

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_user_picture(form.picture.data)
            delete_old_picture(current_user)
            current_user.image_file = picture_file
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

    image_file = url_for(
        'static',
        filename='images/profile_pictures/' + current_user.image_file)
    return render_template('account.html', form=form, image_file=image_file)


@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    if current_user.is_admin:
        return redirect(url_for('root'))
    if request.method == 'POST':  # if posted form from main.html
        ordered_item_id = int(request.form['ordered_item_id'])
        order = Order(item_id=ordered_item_id, user_id=current_user.id)
        db.session.add(order)
        db.session.commit()
    user_orders_list = (db.session.query(Order, Item)
                        .filter(Order.user_id == current_user.id)
                        .join(Item, Order.item_id == Item.id))
    return render_template('cart.html', user_orders_list=user_orders_list)


@app.route('/shopmanagement', methods=['GET', 'POST'])
@login_required
def shopmanagement():
    if current_user.is_admin:
        # try - because there are 2 forms in one template
        try:
            # deletes item from the database by form from itmes table
            deleted_item_id = int(request.form['deleted_item_id'])
            deleted_item = Item.query.filter_by(id=deleted_item_id).first()
            picture_path = os.path.join(
                app.root_path, 'static/images/shop',
                deleted_item.item_image)
            os.remove(picture_path)
            db.session.delete(deleted_item)
            db.session.commit()
            return redirect(url_for('shopmanagement'))
        except:
            # adds a new item
            form = NewItemForm()
            if form.validate_on_submit():
                new_item_image = save_item_picture(form.item_image.data)
                item = Item(
                    item_name=form.item_name.data,
                    item_main_description=form.item_main_description.data,
                    item_points_description=form.item_points_description.data,
                    item_image=new_item_image,
                    item_price=form.item_price.data)
                db.session.add(item)
                db.session.commit()
                return redirect(url_for('shopmanagement'))
        items_list = Item.query.all()
        return render_template(
            'shopmanagement.html',
            items_list=items_list,
            form=form)
    else:
        return redirect(url_for('root'))


@app.route('/orders', methods=['GET', 'POST'])
@login_required
def orders():
    if current_user.is_admin:
        form = OrderStatusForm()
        if form.validate_on_submit():
            order_id = form.order_id.data
            order = db.session.query(Order).filter(
                Order.id == order_id).first()
            order.status = form.status.data
            db.session.commit()
        orders_list = (db.session.query(Order, Item, User)
                       .join(Item, Order.item_id == Item.id)
                       .join(User, Order.user_id == User.id).all())
        return render_template(
            'orders.html',
            orders_list=orders_list,
            form=form)
    else:
        return redirect(url_for('root'))
