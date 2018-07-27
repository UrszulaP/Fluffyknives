from flask import redirect,	url_for, render_template,	request
from app_files import app, db, bcrypt
from app_files.forms import RegistrationForm, LoginForm, UpdateAccountForm
from app_files.db_models import User, Item
from flask_login import login_user, current_user, logout_user, login_required
# secrets do hashowania nazw zdjęć - aby się nie powtarzały
import secrets
# do wyciągnięcia rozszerzenia pliku
import os
# zainstalowano Pillow - do zmiany rozmiaru obrazów
from PIL import Image

# ------------------------------------WIDOKI-----------------------------------------#

@app.route('/')
def root():
	itemsList = Item.query.all()
	return render_template('main.html', itemsList=itemsList)



@app.route('/login', methods=['GET', 'POST'])
def login():
	# sprawdza, czy użytkownik jest już zalogowany - wbudowana funkcja flask_login
	if current_user.is_authenticated:
		return redirect(url_for('root'))
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		# wbudowana funkcja bcrypt, porównująca hasło z bd z hasłem z formularza
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			# wbudowana funkcja flask-login, arg. remember pobiera z checkboxa formularza
			login_user(user, remember=form.remember.data)
			# pobiera argument next z querystringa i po zalogowaniu przekierowuje
			# od razu na żądaną stronę (gdzie wymagane było zalogowanie), nie na root
			# get() zamiast [] - nie wyrzuci błędu tylko None, jeśli parametr nie istnieje
			next_page = request.args.get('next')
			print("next_page", next_page)
			return redirect(next_page) if next_page else redirect(url_for('root'))
		else:
			return render_template('login_failed.html')
	return render_template('login.html', form=form)



@app.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('root'))



@app.route('/register', methods=['GET', 'POST'])
def register():
	# sprawdza, czy użytkownik jest już zalogowany - wbudowana funkcja flask_login
  if current_user.is_authenticated:
    return redirect(url_for('root'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    # user_id stworzy się automatycznie, kolejne
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return render_template('register_ok.html')
  return render_template('register.html', form=form)



# funkcja do uploadu zdjęcia
def save_picture(form_picture):
	# generowanie losowego hasha (8 znaków)
	random_hex = secrets.token_hex(8)
	# oddzielenie nazwy i rozszerzenia pliku
	f_name, file_extension = os.path.splitext(form_picture.filename) # _ - oznaczenie nieużywanej zmiennej
	picture_filename = random_hex + file_extension
	# określenie ścieżki zapisu plików
	picture_path = os.path.join(app.root_path, 'static/images/profile_pictures', picture_filename)
	# zmiana rozmiaru obrazu przy zapisywaniu
	output_size = (125, 125)
	resized_picture = Image.open(form_picture)
	resized_picture.thumbnail(output_size)
	# zapisywanie obrazu do folderu
	resized_picture.save(picture_path)
	# zwraca nazwę pliku, aby zapisać ją w bazie danych
	return picture_filename

@app.route('/account', methods=['GET', 'POST'])
# dekorator z flask_login
@login_required
def account():
	form = UpdateAccountForm()
	# zmiana danych użytkownika
	if form.validate_on_submit():
		# if, bo dodanie pliku obrazu nie jest wymagane
		if form.picture.data:
			picture_file = save_picture(form.picture.data)
			# usuwanie starego zdjęcia
			if current_user.image_file != 'defaultpp.jpg':
				old_picture_path = os.path.join(app.root_path, 'static/images/profile_pictures', current_user.image_file)
				os.remove(old_picture_path)
			current_user.image_file = picture_file
			
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.adress = form.adress.data
		current_user.phone = form.phone.data
		db.session.commit()
		# przy ładowaniu ponownie tej samej strony należy użyć redirect -
		# przy render_template POST będzie wysyłany ponownie (wyskoczy komunikat z pytniem o ponowne przesłanie formularza)
		return render_template('updated.html')
	# wypełnia pola formularza aktualnymi danymi
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
		form.adress.data = current_user.adress
		form.phone.data = current_user.phone
	# określa ścieżkę do zdjęcia profilowego
	image_file = url_for('static', filename='images/profile_pictures/' + current_user.image_file)
	return render_template('account.html', form=form, image_file=image_file)

