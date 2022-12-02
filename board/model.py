from . import db
from . import login_manager
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(32))
    salt = db.Column(db.String(32))

    message = db.relationship('Message', backref='user', lazy='dynamic')

    def __init__(self, username, password, salt=''):
        self.username = username
        self.password = password
        self.salt = salt


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    msg = db.Column(db.String(6000))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, author_id, msg, timestamp):
        self.author_id = author_id
        self.msg = msg
        self.timestamp = timestamp


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
