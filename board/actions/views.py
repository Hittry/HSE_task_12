import datetime

from flask import render_template, redirect, flash
from flask_login import current_user

from board.actions import actions_view
from board.actions.forms import MessageForm, UploadForm, DropForm
from board.model import Message, db
from utils.const import Api


@actions_view.route('/', methods={'get', 'post'})
def index():
    form = MessageForm()
    datetime_now = datetime.datetime.utcnow()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            datetime_now_str = datetime_now.strftime('%Y-%m-%d %H:%M:%S')
            message = Message(current_user.id, form.msg.data, datetime_now_str)
            db.session.add(message)
            db.session.commit()
            flash('Объявление добавлено')
            redirect('/')
        else:
            flash('Не удалось опубликовать объявление. Авторизуйтесь')
            redirect('/')
    messages_for_delete = Message.query.filter(Message.timestamp <
                                               datetime_now - datetime.timedelta(minutes=Api.AGING_TIME)).all()

    for message_for_delete in messages_for_delete:
        Message.query.filter_by(id=message_for_delete.id).delete()
    db.session.commit()
    messages = Message.query.order_by(Message.timestamp.desc()).all()

    return render_template('index.html', form=form, messages=messages)


@actions_view.route('/upload/', methods={'get', 'post'})
def upload():
    form = UploadForm()
    messages = Message.query.filter_by(author_id=current_user.id).all()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            messages_ids = [message.id for message in messages]
            if int(form.ad_id.data) not in messages_ids:
                flash('Это объявление не принадлежит Вам. Введите другой id')
                redirect('/upload/')
            else:
                Message.query.filter_by(id=form.ad_id.data).update(dict(msg=form.msg.data))
                db.session.commit()
                flash('Объявление обновлено')
                redirect('/upload/')
        else:
            flash('Не удалось обновить объявление. Заполните все поля')
            redirect('/upload/')

    return render_template('upload.html', form=form, messages=messages)


@actions_view.route('/drop/', methods={'get', 'post'})
def drop():
    form = DropForm()
    if form.validate_on_submit():
        if current_user.is_authenticated:
            messages = Message.query.filter_by(author_id=current_user.id).all()
            messages_ids = [message.id for message in messages]
            if int(form.ad_id.data) not in messages_ids:
                flash('Это объявление не принадлежит Вам. Введите другой id')
                redirect('/drop/')
            else:
                Message.query.filter_by(id=form.ad_id.data).delete()
                db.session.commit()
                flash('Объявление удалено')
                redirect('/drop/')
        else:
            flash('Не удалось удалить объявление. Заполните все поля')
            redirect('/drop/')

    messages = Message.query.filter_by(author_id=current_user.id).all()
    return render_template('drop.html', form=form, messages=messages)
