import os
import unittest

from first_app.models import *
from first_app import create_app, db

from flask_migrate import Migrate

flask_app = create_app("default")
migrate = Migrate(flask_app, db)


@flask_app.cli.command('test')
def test():
    """What we run"""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
