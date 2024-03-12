from flask import Flask
from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = "hard to unlock"

# csrf = CSRFProtect(app)
from first_app import routes
