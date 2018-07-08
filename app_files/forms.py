from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired("Pole wymagane")])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')
