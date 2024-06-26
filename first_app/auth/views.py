from threading import Thread
from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_mail import Message
from sqlalchemy.exc import IntegrityError
from .forms import LoginForm, RegistrationForm
from . import auth
from .. import db, mail
from ..models import User


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    """
    Confirms user's account with the provided token. Redirects to the index page
    on success or if the user is already confirmed.

    @param token: The token for account confirmation.
    @return: Redirects to the index page.
    """
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token.encode('utf-8')):
        db.session.commit()
        flash('Confirmation was successful.')
    else:
        flash('Link in not valid.')
    return redirect(url_for('main.index'))


@auth.route("/unconfirmed")
def unconfirmed():
    """
    Renders the unconfirmed account page.

    @return: The rendered unconfirmed account page HTML.
    """
    return render_template('unconfirmed.html')


@auth.route("/login", methods=['GET', 'POST'])
def login():
    """
    Handles user login. Checks credentials and logs in the user if valid.
    Redirects to the next page or index. Flashes an error for invalid credentials.

    @return: The login page or a redirection to the next page or index.
    """
    form = LoginForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify(form.password.data):
            login_user(user)
            next_page = request.args.get("next")
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('main.index')
            return redirect(next_page)
        flash('Invalid username or password', 'error')
    return render_template('login.html', form=form)


@auth.route("/logout")
@login_required
def logout():
    """
    Logs out the current user and flashes a logout message. Redirects to the index page.

    @return: A redirection to the index page.
    """
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    """
    Handles new user registration. Creates new user, sets the password, and sends a confirmation email.
    If the data is duplicated, flashes appropriate error messages.

    @return: The registration page with the form, or a redirection to the login page upon successful registration.
    """
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            new_user = User(email=form.email.data, username=form.username.data,
                            gender=form.gender.data)
            db.session.add(new_user)
            new_user.set_password(form.password.data)
            db.session.commit()

            print('форма успешно обработана')

            email = request.form['email']
            send_mail(email, "Успешная регистрация", "registration_email", {'username': new_user.username})
            flash('Проверьте почту для подтверждения регистрации.')

            return redirect(url_for('auth.login'))

        except IntegrityError as e:
            if "key 'email'" in str(e):
                flash('Пользователь с таким email уже существует', 'email_error')
            elif "key 'username'" in str(e):
                flash('Пользователь с таким именем уже существует', 'username_error')
            db.session.rollback()
            return redirect(url_for('auth.registration'))

    return render_template('registration.html', form=form)


def send_mail(to, subject, template, kwargs):
    """
    Sends a confirmation email to the user with a generated token.

    @param to: Recipient email address.
    @param subject: Subject of the email.
    @param template: Template for the email body.
    @param kwargs: Additional keyword arguments for the template.
    """
    user = User.query.filter_by(email=to).first()
    token = user.generate_confirmation_token()
    msg = Message(subject,
                  sender=current_app.config['MAIL_USERNAME'],
                  recipients=[to])
    msg.html = render_template(template + ".html", token=token.decode('utf-8'), **kwargs)
    from app import flask_app
    thread = Thread(target=send_async_email, args=[flask_app, msg])
    thread.start()


def send_async_email(app, msg):
    """
    Sends an email asynchronously within the application context.

    @param app: The Flask application instance.
    @param msg: The email message to send.
    """
    with app.app_context():
        mail.send(msg)
