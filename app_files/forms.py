from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed   # do uploadu obrazów
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app_files.db_models import User

# Formularz rejestracji
class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika',
                           validators=[DataRequired("Pole wymagane"), 
                           Length(min=2, max=20, message="Nazwa powinna zawierać od %(min)d do %(max)d znaków")])
    email = StringField('Email',
                        validators=[DataRequired("Pole wymagane"), 
                        Email("Nieprawidłowy adres e-mail")])
    password = PasswordField('Hasło', validators=[DataRequired("Pole wymagane")])
    confirm_password = PasswordField('Potwierdź hasło',
                                     validators=[DataRequired("Pole wymagane"), 
                                     EqualTo('password', message="Hasła nie zgadzają się")])
    submit = SubmitField('Utwórz konto')

    # custom validation - sprawdza, czy wprowadzono unikalną wartość 
    # (nie trzeba wywoływać - klasa FlaskForm robi to automatycznie)
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first() # jeśli nie ma, zwróci None
        if user:
            raise ValidationError("Nazwa użytkownika jest już zajęta")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first() # jeśli nie ma, zwróci None
        if email:
            raise ValidationError("Konto z podanym adresem e-mail już istnieje")


# Formularz logowania
class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired("Pole wymagane")])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


# Formularz zmiany danych konta
class UpdateAccountForm(FlaskForm):
    username = StringField('Nazwa użytkownika',
                           validators=[DataRequired("Pole wymagane"), 
                           Length(min=2, max=20, message="Nazwa powinna zawierać od %(min)d do %(max)d znaków")])
    email = StringField('Email',
                        validators=[DataRequired("Pole wymagane"), 
                        Email("Nieprawidłowy adres e-mail")])
    picture = FileField('Zaktualizuj zdjęcie profilowe', 
                        validators=[FileAllowed(['jpg', 'png'], "Dozwolony format pliku to .jpg lub .png")])
    adress = StringField('Adres do wysyłki', validators=[Length(min=2, max=200, message="Adres powinien zawierać od %(min)d do %(max)d znaków")])
    phone = StringField('Numer telefonu', validators=[Length(min=9, max=20, message="Numer powinien zawierać od %(min)d do %(max)d znaków")])
    submit = SubmitField('Zaktualizuj')

    # custom validation - sprawdza, czy wprowadzono unikalną wartość - tylko gdy wprowadzono inną niż aktualna
    # (nie trzeba wywoływać - klasa FlaskForm robi to automatycznie)
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first() # jeśli nie ma, zwróci None
            if user:
                raise ValidationError("Nazwa użytkownika jest już zajęta")

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first() # jeśli nie ma, zwróci None
            if email:
                raise ValidationError("Konto z podanym adresem e-mail już istnieje")