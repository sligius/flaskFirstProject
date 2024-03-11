from flask import render_template

from first_app import app


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
