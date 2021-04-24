from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, \
    RadioField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, \
    ValidationError
from app_files.db_models import User, Item


class RegistrationForm(FlaskForm):
    username = StringField(
        'Nazwa użytkownika',
        validators=[
            DataRequired("Pole wymagane"),
            Length(
                min=2, max=20,
                message="Nazwa powinna zawierać od %(min)d do %(max)d znaków")])

    email = StringField(
        'Email',
        validators=[
            DataRequired("Pole wymagane"),
            Email("Nieprawidłowy adres e-mail")])

    password = PasswordField(
        'Hasło',
        validators=[DataRequired("Pole wymagane")])

    confirm_password = PasswordField(
        'Potwierdź hasło',
        validators=[
            DataRequired("Pole wymagane"),
            EqualTo('password', message="Hasła nie zgadzają się")])

    submit = SubmitField('Utwórz konto')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Nazwa użytkownika jest już zajęta")

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("Konto z podanym adresem e-mail już istnieje")


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Hasło', validators=[DataRequired("Pole wymagane")])
    remember = BooleanField('Zapamiętaj mnie')
    submit = SubmitField('Zaloguj')


class UpdateAccountForm(FlaskForm):
    username = StringField(
        'Nazwa użytkownika',
        validators=[
            DataRequired("Pole wymagane"),
            Length(
                min=2, max=20,
                message="Nazwa powinna zawierać od %(min)d do %(max)d znaków")])

    email = StringField(
        'Email',
        validators=[DataRequired("Pole wymagane"),
                    Email("Nieprawidłowy adres e-mail")])

    picture = FileField(
        'Zaktualizuj zdjęcie profilowe',
        validators=[
            FileAllowed(['jpg', 'png'], "Dozwolony format pliku to .jpg lub .png")])

    adress = StringField(
        'Adres do wysyłki',
        validators=[
            Length(
                max=200,
                message="Adres powinien zawierać od %(min)d do %(max)d znaków")])

    phone = StringField(
        'Numer telefonu',
        validators=[
            Length(
                max=20,
                message="Numer powinien zawierać od %(min)d do %(max)d znaków")])

    submit = SubmitField('Zaktualizuj')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Nazwa użytkownika jest już zajęta")

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                raise ValidationError("Konto z podanym adresem e-mail już \
                                      istnieje")


class OrderStatusForm(FlaskForm):
    status = RadioField(
        'Aktualizuj status',
        choices=[('W trakcie realizacji',
                  'W trakcie realizacji'),
                 ('Wysłano', "Wysłano"),
                 ('Dostarczono', 'Dostarczono')])
    order_ID = StringField('Nr zamówienia')
    submit = SubmitField('Zaktualizuj')


class NewItemForm(FlaskForm):
    item_name = StringField(
        'Nazwa',
        validators=[
            DataRequired("Pole wymagane"),
            Length(
                min=2, max=30,
                message="Nazwa powinna zawierać od %(min)d do %(max)d znaków")])

    item_main_description = TextAreaField(
        'Opis główny',
        validators=[
            Length(
                max=200,
                message="Opis powinien zawierać do %(max)d znaków")])

    item_points_description = TextAreaField(
        'Opis dodatkowy',
        validators=[
            Length(
                max=300,
                message="Opis powinien zawierać do %(max)d znaków")])

    item_image = FileField(
        'Obraz',
        validators=[
            DataRequired("Pole wymagane"),
            FileAllowed(
                ['jpg', 'png'],
                "Dozwolony format pliku to .jpg lub .png")])

    item_price = FloatField(
        'Cena',
        validators=[
            DataRequired("Pole wymagane. Dozwolone formaty ceny: 100 / 100.00")])

    submit = SubmitField('Dodaj')

    def validate_item_name(self, item_name):
        item = Item.query.filter_by(item_name=item_name.data).first()
        if item:
            raise ValidationError("Przedmiot o podanej nazwie już istnieje")
