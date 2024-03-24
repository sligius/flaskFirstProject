from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo


class SimpleForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Имя пользователя", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    confirm_password = PasswordField("Повторите пароль", validators=[DataRequired(), EqualTo('password')])
    gender = SelectField("Пол", choices=[('male', 'Мужской'), ('female', 'Женский'), ('none', 'Не указывать')],
                         validators=[DataRequired()])
    submit = SubmitField("Готово")
