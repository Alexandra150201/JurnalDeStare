from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_user import UserManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "helloworld"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['USER_EMAIL_SENDER_EMAIL'] = "noreply@example.com"
    db.init_app(app)

    from website.controller.pacientView import ControllerPacient
    from website.controller.auth import ControllerAuth
    from website.controller.terapeutView import ControllerTerapeut
    from website.domain.models import User, Post,Terapeut

    controllerAuth = ControllerAuth()
    controllerPacient = ControllerPacient()
    controllerTerapeut = ControllerTerapeut()
    app.register_blueprint(controllerPacient.views, url_prefix="/")
    app.register_blueprint(controllerAuth.auth, url_prefix="/")
    app.register_blueprint(controllerTerapeut.terapeutView, url_prefix="/")

    user_manager = UserManager(app, db, User)

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists("website/" + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Created database!")
