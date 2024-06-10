from flask import render_template, redirect, url_for, request
from flask_login import current_user
from . import main
from .. import db
from ..models import User, Book


@main.route("/")
@main.route("/index")
def index():
    """
    Renders the index page.

    @return: The rendered index page HTML.
    """
    return render_template('index.html')


@main.route('/profile/<username>')
def profile(username):
    """
    Displays the user's profile and book information if specified.

    @param username: The username for which the profile is displayed.
    @return: The user's profile page with book information.
    """
    user = User.query.filter_by(username=username).first_or_404()
    books = Book.query.all()
    if user.book_id:
        book_title = Book.query.filter_by(id=user.book_id).first().title
    else:
        book_title = None
    return render_template('reader_profile.html', reader=user, book_title=book_title, books=books)


@main.route('/profile/<username>/set_favorite_book', methods=['POST'])
def set_favorite_book(username):
    """
    Sets the favorite book for the user if they are a confirmed user.

    @param username: The username for which the favorite book is being set.
    @return: Redirects to the user's profile page or unconfirmed user page.
    """
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
    """
    Injects the current user into the context for use in templates.

    @return: A dictionary containing the current user under the key 'reader'.
    """
    user = current_user
    return dict(reader=user)
