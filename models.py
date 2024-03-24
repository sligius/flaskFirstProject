from first_app import db


# flask db migrate -m "fix_tables"
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


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))

    def __repr__(self):
        return f"<users {self.id}>"


'''
class FavoriteBook(db.Model):
    __tablename__ = 'favorite_books'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)

    def __repr__(self):
        return f"<>"
'''
