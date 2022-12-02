from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

from utils.const import DbConnection, Api
import pymysql
pymysql.install_as_MySQLdb()

app = None
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
migrate = Migrate()


def create_app():
    global app
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = DbConnection.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SECRET_KEY'] = Api.SECRET_KEY

    db.init_app(app)
    migrate.init_app(app, db)
    bootstrap.init_app(app)
    login_manager.init_app(app)

    from .auth import auth_view as auth_blueprint
    from .actions import actions_view as actions_blueprint

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(actions_blueprint)
    return app
