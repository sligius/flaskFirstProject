import unittest
from first_app.models import User


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='light')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password='light')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password='light')
        self.assertTrue(u.verify('light'))
        self.assertFalse(u.verify('dark'))

    def test_password_salts_are_random(self):
        u = User(password='light')
        u2 = User(passsword='light')
        self.assertTrue(u.password_hash != u2.password_hash)
