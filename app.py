from flask import (
	Flask,
	redirect,
	url_for,
	#jsonify,
	render_template,
	request,
	session,
	g,)
from functools import wraps
import sqlite3
import json

app = Flask(__name__)
app.secret_key = "any random string"

# -----------------------------POŁĄCZENIE Z BAZĄ DANYCH------------------------------#

DATABASE = 'db/database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# -------------------------------FUNKCJE DO LOGOWANIA--------------------------------#

def requires_user_session(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('username'):
            #print("requires_user_session", session)
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return wrapper


def check_auth(username, password):
	try:
		db = get_db()
		data = db.execute('SELECT * FROM users WHERE UserLogin = ?', (username,)).fetchall()
		check_username = data[0][1]
		check_password = data[0][2]
	except:
		return False
	return username == check_username and password == check_password


# ------------------------------------WIDOKI-----------------------------------------#

@app.route('/')
def root():
	
	db = get_db()
	data = db.execute('SELECT * FROM items').fetchall()

	itemsList = []
	for i in data:
		itemsList.append(i)
		itemsList_json = json.dumps(itemsList)

	return render_template('main.html', itemsList = itemsList)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		if 'username' in session:
			return redirect(url_for('hello'))
		return render_template('login.html')

	if request.method == 'POST':
		username = request.form['userID']
		password = request.form['userPass']

		if check_auth(username, password):
			#print("przed", session)
			session['username'] = username
			#print("po", session)
			return redirect(url_for('hello'))
		else:
			return render_template('login_failed.html')


@app.route('/hello')
@requires_user_session
def hello():
	name = session['username']
	#print("hello", session)
	return render_template('hello.html', name = name)



@app.route('/logout')
@requires_user_session
def logout():
	del session['username']
	#print("logout", session)
	return redirect(url_for('root'))



@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'GET':
		if 'username' in session:
			return redirect(url_for('hello'))
		return render_template('register.html')

	if request.method == 'POST':
		username = request.form['userID']
		password = request.form['userPass']
		if username == "":
			return render_template('register_failed.html', message="Nie wprowadzono loginu")
		if password == "":
			return render_template('register_failed.html', message="Nie wprowadzono hasła")
		
		# pobiera max id z bazy, ustawia nowe id na kolejne
		db = get_db()
		try:
			data = db.execute('SELECT MAX(UserID) FROM users').fetchall()
			next_user_id = str(int(data[0][0]) + 1)
		except:
			next_user_id = 1
		
		# dodaje nowego użytkownika do bazy
		try:
			data = db.execute('INSERT INTO users (UserID, UserLogin, UserPassword) VALUES (?,?,?)', (next_user_id, username, password)).fetchall()
			db.commit()
		except:
			return render_template('register_failed.html', message="Nazwa użytkownika jest już zajęta")
		return "Zarejestrowano"




if __name__ == '__main__':
	app.run(debug=True, use_debugger=False)