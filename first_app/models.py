from authlib.jose import JsonWebSignature
from flask_login import UserMixin

from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash


# flask db migrate -m "edit_token"
# flask db upgrade


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    genres = db.Column(db.String(100))

    users = db.relationship('User', backref='fav_book')

    def repr(self):
        return f"<Book {self.id}>"


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    gender = db.Column(db.String(10), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    def generate_confirmation_token(self):
        jws = JsonWebSignature()
        protected = {'alg': 'HS256'}
        payload = self.id
        secret = 'secret'
        return jws.serialize_compact(protected, payload, secret)

    def confirm(self, token):
        jws = JsonWebSignature()
        data = jws.deserialize_compact(s=token, key='secret')
        if data.payload.decode('utf-8') != str(self.id):
            print("it's not your token")
            return False
        else:
            self.confirmed = True
            db.session.add(self)
            return True

    @property
    def password(self):
        raise AttributeError("password not enable to read")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def verify(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<users {self.id}>"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


'''
class FavoriteBook(db.Model):
    __tablename__ = 'favorite_books'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)

    def __repr__(self):
        return f"<>"
'''
