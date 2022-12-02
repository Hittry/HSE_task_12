from flask_wtf import FlaskForm
from wtforms.fields import simple
from wtforms import validators
from wtforms import SubmitField


class MessageForm(FlaskForm):
    msg = simple.TextAreaField(
        label='Введите объявление',
        validators=[
            validators.DataRequired(),
        ],
    )
    submit = SubmitField(label='Опубликовать')


class UploadForm(FlaskForm):
    ad_id = simple.TextAreaField(
        label='Id объявления',
        validators=[
            validators.DataRequired(),
        ],
    )
    msg = simple.TextAreaField(
        label='Введите новый текст объявления',
        validators=[
            validators.DataRequired(),
        ],
    )
    submit = SubmitField(label='Обновить')


class DropForm(FlaskForm):
    ad_id = simple.TextAreaField(
        label='Id объявления',
        validators=[
            validators.DataRequired(),
        ],
    )
    submit = SubmitField(label='Удалить')
