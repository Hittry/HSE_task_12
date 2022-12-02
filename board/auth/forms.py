from flask_wtf import FlaskForm
from wtforms.fields import simple
from wtforms import validators
from wtforms import widgets
from wtforms import SubmitField


class LoginForm(FlaskForm):
    username = simple.StringField(
        label='Имя пользователя',
        validators=[
            validators.DataRequired(message='Имя пользователя не может быть пустым'),
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control'}
    )
    password = simple.PasswordField(
        label='Пароль',
        validators=[
            validators.DataRequired(message='Пароль не может быть пустым'),
            validators.Length(min=6, message='Длина пароля должна быть меньше 6 символов'),
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )
    login = SubmitField(label='Логин')


class RegisterForm(FlaskForm):
    username = simple.StringField(
        label='Имя пользователя',
        validators=[
            validators.DataRequired(message='Имя пользователя не может быть пустым'),
        ],
        widget=widgets.TextInput(),
        render_kw={'class': 'form-control'},
        default='test'
    )
    password = simple.PasswordField(
        label='Пароль',
        validators=[
            validators.DataRequired(message='Пароль не может быть пустым'),
            validators.Length(min=6, message='Длина пароля должна быть меньше 6 символов'),
            validators.EqualTo('confirm', message='Пароли не совпадают')
        ],
        widget=widgets.PasswordInput(),
        render_kw={'class': 'form-control'}
    )
    confirm = simple.PasswordField('Повторите пароль')
    submit = SubmitField(label='Регистрация')
