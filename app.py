import unittest

from first_app import create_app

flask_app = create_app("default")


@flask_app.cli.command('test')
def test():
    """What we run"""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
