from flask import render_template, redirect, url_for, session, flash
from sqlalchemy.exc import IntegrityError

from first_app.forms import SimpleForm
from first_app import app, db
from models import User


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')


movies = {
    'godfather': 'Крёстный отец - Классический мафиозный фильм режиссера Фрэнсиса Форда Коппола.',
    'shawshank': 'Побег из Шоушенка - Один из величайших фильмов, когда-либо снятых, режиссёр Фрэнк Дарабонт.',
    'inception': 'Начало - Умопомрачительный научно-фантастический фильм режиссёра Кристофера Нолана.'
}


@app.route("/movie/<movie_title>")
def show_movie(movie_title):
    if movie_title in movies:
        return f'<h1>{movie_title.capitalize()}</h1>' \
               f'<p>{movies[movie_title]}</p>'
    else:
        return "Фильм не найден."


@app.route("/table")
def show_table():
    return '''
    <table>
      <tr><td>1</td><td>че то</td></tr>
      <tr><td>2</td><td>еще че то</td></tr>
      <tr><td>3</td><td>ну и напоследок тоже че то</td></tr>
    </table>
    '''


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('405.html'), 405


@app.route('/form', methods=['GET', 'POST'])
def testForm():
    form = SimpleForm()
    if form.validate_on_submit():
        try:
            print('test')
            new_user = User(email=form.email.data, username=form.username.data, password=form.password.data,
                            gender=form.gender.data)
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            session['username'] = new_user.username
            session['email'] = form.email.data
            session['gender'] = form.gender.data
            print('форма успешно обработана')
            return redirect(url_for('show_data'))
        except IntegrityError as e:
            if "key 'email'" in str(e):
                flash('Пользователь с таким email уже существует', 'email_error')
            elif "key 'username'" in str(e):
                flash('Пользователь с таким именем уже существует', 'username_error')
            db.session.rollback()
            return redirect(url_for('testForm'))
    return render_template('form.html', form=form)


@app.route('/show_data')
def show_data():
    user_id = session.get('user_id')
    username = session.get('username')
    email = session.get('email')
    gender = session.get('gender')
    return render_template('display_data.html', user_id=user_id, username=username, email=email, gender=gender)
