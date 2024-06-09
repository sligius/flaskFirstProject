from flask import render_template, redirect, url_for, session, request
from flask_login import current_user, login_required
from . import main
from .. import db
from ..decorators import permission_required
from ..models import User, Book, Permission


@main.route("/")
@main.route("/index")
def index():
    return render_template('index.html')


movies = {
    'godfather': 'Крёстный отец - Классический мафиозный фильм режиссера Фрэнсиса Форда Коппола.',
    'shawshank': 'Побег из Шоушенка - Один из величайших фильмов, когда-либо снятых, режиссёр Фрэнк Дарабонт.',
    'inception': 'Начало - Умопомрачительный научно-фантастический фильм режиссёра Кристофера Нолана.'
}


@main.route("/movie/<movie_title>")
def show_movie(movie_title):
    if movie_title in movies:
        return f'<h1>{movie_title.capitalize()}</h1>' \
               f'<p>{movies[movie_title]}</p>'
    else:
        return "Фильм не найден."


@main.route("/table")
def show_table():
    return '''
    <table>
      <tr><td>1</td><td>че то</td></tr>
      <tr><td>2</td><td>еще че то</td></tr>
      <tr><td>3</td><td>ну и напоследок тоже че то</td></tr>
    </table>
    '''


@main.route('/show_data')
def show_data():
    user_id = session.get('user_id')
    username = session.get('username')
    email = session.get('email')
    gender = session.get('gender')
    return render_template('display_data.html', user_id=user_id, username=username, email=email, gender=gender)


@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE)
def for_moderator():
    return 'For moderator'


@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    books = Book.query.all()
    if user.book_id:
        book_title = Book.query.filter_by(id=user.book_id).first().title
    else:
        book_title = None
    return render_template('reader_profile.html', reader=user, book_title=book_title, books=books)


@main.route('/profile/<username>/set_favorite_book', methods=['POST'])
def set_favorite_book(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.confirmed:
        book_id = request.form.get('book_id')
        if book_id:
            user.book_id = book_id
        else:
            user.book_id = None
        db.session.commit()
        return redirect(url_for('main.profile', username=username))
    else:
        return redirect(url_for('auth.unconfirmed'))


@main.app_context_processor
def inject_reader():
    user = current_user
    return dict(reader=user)
