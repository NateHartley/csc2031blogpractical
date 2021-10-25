import logging
from datetime import datetime
from flask import Blueprint, render_template, flash, redirect, url_for, session, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db
from blog.views import blog
from models import User
from users.forms import RegisterForm, LoginForm
import pyotp

users_blueprint = Blueprint('users', __name__, template_folder='templates')


@users_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # if this returns a user, then the email already exists in database
        user = User.query.filter_by(username=form.username.data).first()

        # if a user is found redirect user back to signup page so user can try again
        if user:
            flash('Username address already exists')
            return render_template('register.html', form=form)

        # create a new user with the form data
        new_user = User(username=form.username.data,
                        password=form.password.data,
                        role='user',
                        pinkey=form.pinkey.data)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        logging.warning('SECURITY - User registration [%s, %s]', form.username.data, request.remote_addr)

        return redirect(url_for('users.login'))

    return render_template('register.html', form=form)


@users_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # if session attribute logins does not exist create attribute logins
    if not session.get('logins'):
        session['logins'] = 0
    # if login attempts is 3 or more create an error message
    elif session.get('logins') >= 3:
        flash('Number of incorrect logins exceeded')

    form = LoginForm()

    if form.validate_on_submit():

        # increase login attempts by 1
        session['logins'] += 1

        user = User.query.filter_by(username=form.username.data).first()

        if not user or not check_password_hash(user.password, form.password.data):

            # if no match create appropriate error message based on login attempts
            if session['logins'] == 3:
                flash('Number of incorrect logins exceeded')
            elif session['logins'] == 2:
                flash('Please check your login details and try again. 1 login attempt remaining')
            else:
                flash('Please check your login details and try again. 2 login attempts remaining')

            return render_template('login.html', form=form)

        if pyotp.TOTP(user.pinkey).verify(form.pin.data):
            session['logins'] = 0
            login_user(user)
            user.last_logged_in = user.current_logged_in
            user.current_logged_in = datetime.now()
            db.session.commit()
            logging.warning('SECURITY - Log in [%s, %s, %s]', current_user.id, current_user.username, request.remote_addr)

            # direct to role appropriate page
            if current_user.role == 'admin':
                return redirect(url_for('admin.admin'))
            else:
                return redirect(url_for('blog.blog'))

        else:
            flash("You have supplied an invalid 2FA token!", "danger")

    return render_template('login.html', form=form)


@users_blueprint.route('/logout')
@login_required
def logout():
    logging.warning('SECURITY - Log out [%s, %s, %s]', current_user.id, current_user.username, request.remote_addr)

    logout_user()
    return redirect(url_for('index'))
