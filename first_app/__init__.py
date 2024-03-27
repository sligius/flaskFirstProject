import os

from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from flask import Flask
from flask_wtf import CSRFProtect

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = "hard to unlock"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True

mail = Mail(app)

# csrf = CSRFProtect(app)
from models import *

migrate = Migrate(app, db)
from first_app import routes
