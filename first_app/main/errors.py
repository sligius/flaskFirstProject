from flask import render_template
from . import main


@main.app_errorhandler(405)
def method_not_allowed(error):
    return render_template('405.html'), 405
