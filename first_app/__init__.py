from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import config

db = SQLAlchemy()
mail = Mail()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    print(main_blueprint)

    app.register_blueprint(main_blueprint, config=config)

    from .auth import auth as auth_blueprint
    print(auth_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    print(app.url_map)
    return app


