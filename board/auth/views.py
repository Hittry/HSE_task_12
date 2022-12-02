import hashlib
import random

from flask import render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, login_required

from board.auth import auth_view
from board.auth.forms import LoginForm, RegisterForm
from board.model import User, db


@auth_view.route('/login/', methods={'get', 'post'})
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None:
            md5_hash = hashlib.md5()
            md5_hash.update(str.encode(form.password.data + user.salt))
            if md5_hash.hexdigest() != user.password:
                flash('Неверный пароль')
                return redirect('/login')
            login_user(user)
            return redirect('/')
        else:
            flash('Неверное имя пользователя и/или пароль')
    return render_template('login.html', form=form)


@auth_view.route('/register/', methods={'get', 'post'})
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is not None:
                flash('Данное имя пользователя уже используется')
                return redirect('/register')

            salt = ''.join(random.sample('0123456789abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 10))
            md5_hash = hashlib.md5()
            md5_hash.update(str.encode(form.password.data + salt))
            password = md5_hash.hexdigest()
            user = User(form.username.data, password, salt)
            db.session.add(user)
            db.session.commit()
            flash('Успешная регистрация')
            return redirect(url_for('auth_view.login'))
        flash('Пароли не совпадают')
    return render_template('register.html', form=form)


@auth_view.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('Успешный выход из системы')
    return redirect(url_for('auth_view.login'))
