from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Готово")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    confirm_password = PasswordField("Повторите пароль", validators=[DataRequired(), EqualTo('password')])
    gender = SelectField("Пол", choices=[('male', 'Мужской'), ('female', 'Женский'), ('none', 'Не указывать')],
                         validators=[DataRequired()])
    submit = SubmitField("Готово")
