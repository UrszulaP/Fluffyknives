from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed   # for images uplading
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app_files.db_models import User, Item

#------------------------------ REGISTRATION FORM ----------------------------------#

class RegistrationForm(FlaskForm):
	username = StringField('Nazwa użytkownika',
							validators=[DataRequired("Pole wymagane"), 
							Length(min=2, max=20, message="Nazwa powinna zawierać od %(min)d do %(max)d znaków")])
	email = StringField('Email',
						validators=[DataRequired("Pole wymagane"), 
						Email("Nieprawidłowy adres e-mail")])
	password = PasswordField('Hasło', validators=[DataRequired("Pole wymagane")])
	confirmPassword = PasswordField('Potwierdź hasło',
									 validators=[DataRequired("Pole wymagane"), 
									 EqualTo('password', message="Hasła nie zgadzają się")])
	submit = SubmitField('Utwórz konto')

	# custom validation - checks if the given value is uniqe
	# no need to call this function - FlaskForm class makes it automatically
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first() # returns None if it doesn`t exist
		if user:
			raise ValidationError("Nazwa użytkownika jest już zajęta")

	def validate_email(self, email):
		email = User.query.filter_by(email=email.data).first() # returns None if it doesn`t exist
		if email:
			raise ValidationError("Konto z podanym adresem e-mail już istnieje")


#---------------------------------- LOGIN FORM -------------------------------------#

class LoginForm(FlaskForm):
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Hasło', validators=[DataRequired("Pole wymagane")])
	remember = BooleanField('Zapamiętaj mnie')
	submit = SubmitField('Zaloguj')


#------------------------------ ACCOUNT UPDATE FORM --------------------------------#

class UpdateAccountForm(FlaskForm):
	username = StringField('Nazwa użytkownika',
							validators=[DataRequired("Pole wymagane"), 
							Length(min=2, max=20, message="Nazwa powinna zawierać od %(min)d do %(max)d znaków")])
	email = StringField('Email',
						validators=[DataRequired("Pole wymagane"), 
						Email("Nieprawidłowy adres e-mail")])
	picture = FileField('Zaktualizuj zdjęcie profilowe', 
						validators=[FileAllowed(['jpg', 'png'], "Dozwolony format pliku to .jpg lub .png")])
	# Length(min=...) forces to enter value, even if there`s no DataRequired
	adress = StringField('Adres do wysyłki', 
						validators=[Length(max=200, message="Adres powinien zawierać od %(min)d do %(max)d znaków")])
	phone = StringField('Numer telefonu', 
						validators=[Length(max=20, message="Numer powinien zawierać od %(min)d do %(max)d znaków")])
	submit = SubmitField('Zaktualizuj')

	# custom validation - checks if the given value is uniqe - only if given different from the current value
	# no need to call this function - FlaskForm class makes it automatically
	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first() # returns None if it doesn`t exist
			if user:
				raise ValidationError("Nazwa użytkownika jest już zajęta")

	def validate_email(self, email):
		if email.data != current_user.email:
			email = User.query.filter_by(email=email.data).first() # returns None if it doesn`t exist
			if email:
				raise ValidationError("Konto z podanym adresem e-mail już istnieje")


#------------------------------ ORDER STATUS FORM ----------------------------------#

class OrderStatusForm(FlaskForm):
	status = RadioField('Aktualizuj status', choices=[('W trakcie realizacji', 'W trakcie realizacji'),
		('Wysłano', "Wysłano"), ('Dostarczono', 'Dostarczono')])
	orderID = StringField('Nr zamówienia')
	submit = SubmitField('Zaktualizuj')


#-------------------------------- NEW ITEM FORM ------------------------------------#

class NewItemForm(FlaskForm):
	itemName = StringField('Nazwa', 
							validators=[DataRequired("Pole wymagane"), 
							Length(min=2, max=30, message="Nazwa powinna zawierać od %(min)d do %(max)d znaków")])
	# Length(min=...) forces to enter value, even if there`s no DataRequired
	itemMainDescription = TextAreaField('Opis główny', 
							validators=[Length(max=200, message="Opis powinien zawierać do %(max)d znaków")])
	itemPointsDescription = TextAreaField('Opis dodatkowy', 
							validators=[Length(max=300, message="Opis powinien zawierać do %(max)d znaków")])
	itemImage = FileField('Obraz', 
							validators=[DataRequired("Pole wymagane"), 
							FileAllowed(['jpg', 'png'], "Dozwolony format pliku to .jpg lub .png")])
	itemPrice = FloatField('Cena', validators=[DataRequired("Pole wymagane. Dozwolone formaty ceny: 100 / 100.00")])
	submit = SubmitField('Dodaj')

	# custom validation - checks if the given value is uniqe - only if given different from the current value
	# no need to call this function - FlaskForm class makes it automatically
	def validate_itemName(self, itemName):
		item = Item.query.filter_by(itemName=itemName.data).first() # returns None if it doesn`t exist
		if item:
			raise ValidationError("Przedmiot o podanej nazwie już istnieje")

