from flask import render_template, redirect, url_for, session, flash, request, current_app
from flask_login import current_user
from flask_mail import Message
from . import main
from .. import mail
from ..models import User, Book


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


def send_mail(to, subject, template, kwargs):
    msg = Message(subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template + ".html", **kwargs)

    mail.send(msg)


@main.route('/show_data')
def show_data():
    user_id = session.get('user_id')
    username = session.get('username')
    email = session.get('email')
    gender = session.get('gender')
    return render_template('display_data.html', user_id=user_id, username=username, email=email, gender=gender)


@main.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user.book_id:
        book_title = Book.query.filter_by(id=user.book_id).first().title
    else:
        book_title = None
    return render_template('reader_profile.html', reader=user, book_title=book_title)


@main.app_context_processor
def inject_reader():
    user = current_user
    return dict(reader=user)
