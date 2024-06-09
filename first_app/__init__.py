import flask_admin
from flask_admin import Admin, expose
from flask_admin.contrib import sqla
from flask_login import LoginManager, current_user
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, abort, redirect, url_for, request
from config import config
from authlib.integrations.flask_client import OAuth

db = SQLAlchemy()
mail = Mail()
oauth = OAuth()
migrate = Migrate()
admin = Admin()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return (current_user.is_active and
                current_user.is_authenticated and
                current_user.can(16)
                )

    def _handle_view(self, name, **kwargs):
        if not self.is_accessible():
            if current_user.is_authenticated:
                abort(403)
            else:
                return redirect(url_for('main.index', next=request.url))


class MyAdminIndexView(flask_admin.AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for('auth.login'))
        return super(MyAdminIndexView, self).index()


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    oauth.init_app(app)
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint, config=config)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    admin = flask_admin.Admin(app, index_view=MyAdminIndexView())
    from first_app.models import User, Book
    admin.add_view(MyModelView(User, db.session))
    admin.add_view(MyModelView(Book, db.session))

    return app
