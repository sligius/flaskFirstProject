import unittest
from first_app.models import User, Permission, AnonymousUser


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User()
        u.set_password('light')
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User()
        u.set_password('light')
        with self.assertRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User()
        u.set_password('light')
        self.assertTrue(u.verify('light'))
        self.assertFalse(u.verify('dark'))

    def test_password_salts_are_random(self):
        u = User()
        u.set_password('light')
        u2 = User()
        u2.set_password('dark')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_user_role(self):
        user = User(email='test@gmail.com')
        user.set_password('light')
        self.assertTrue(user.can(Permission.FOLLOW))
        self.assertTrue(user.can(Permission.COMMENT))
        self.assertTrue(user.can(Permission.WRITE))
        self.assertFalse(user.can(Permission.MODERATE))
        self.assertFalse(user.can(Permission.ADMIN))

    def test_anonim(self):
        user = AnonymousUser()
        self.assertFalse(user.can(Permission.FOLLOW))
        self.assertFalse(user.can(Permission.COMMENT))
        self.assertFalse(user.can(Permission.WRITE))
        self.assertFalse(user.can(Permission.MODERATE))
        self.assertFalse(user.can(Permission.ADMIN))
