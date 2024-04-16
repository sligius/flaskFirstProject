from flask import render_template, redirect, url_for, flash, request, session, current_app
from flask_login import login_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError

from .forms import LoginForm, RegistrationForm
from . import auth
from .. import db
from ..models import User
from first_app.main.views import send_mail


@auth.route("/login", methods=['GET', 'POST'])
def login():
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
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            print('test')
            print(User)
            print(form.email.data, form.username.data, form.password.data, form.gender.data)

            new_user = User(email=form.email.data, username=form.username.data, password=form.password.data,
                            gender=form.gender.data)
            print(new_user.email, new_user.id, new_user.password_hash)
            db.session.add(new_user)
            db.session.commit()

            session['user_id'] = new_user.id
            session['username'] = form.username.data
            session['email'] = form.email.data
            session['gender'] = form.gender.data

            print('форма успешно обработана')

            email = request.form['email']

            send_mail(email, "Успешная регистрация", "registration_email", {'username': new_user.username})

            return redirect(url_for('auth.login'))
        except IntegrityError as e:
            if "key 'email'" in str(e):
                flash('Пользователь с таким email уже существует', 'email_error')
            elif "key 'username'" in str(e):
                flash('Пользователь с таким именем уже существует', 'username_error')
            db.session.rollback()
            return redirect(url_for('auth.registration'))
    return render_template('registration.html', form=form)
