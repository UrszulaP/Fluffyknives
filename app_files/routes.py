from flask import redirect,	url_for, render_template,	request
from app_files import app, db, bcrypt
from app_files.forms import RegistrationForm, LoginForm
from app_files.db_models import User
from flask_login import login_user, current_user, logout_user, login_required


# ------------------------------------WIDOKI-----------------------------------------#

@app.route('/')
def root():
	# db = get_db()
	# data = db.execute('SELECT * FROM items').fetchall()

	# itemsList = []
	# for i in data:
	# 	itemsList.append(i)
	# 	itemsList_json = json.dumps(itemsList)

	# return render_template('main.html', itemsList = itemsList)
	return render_template('main.html')



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


@app.route('/account')
@login_required
def account():
	return render_template('account.html')