from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app_files.db_models import User

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


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired("Pole wymagane")])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')
