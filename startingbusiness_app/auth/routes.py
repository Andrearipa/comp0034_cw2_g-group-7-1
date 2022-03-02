from flask import Blueprint, render_template, flash, redirect, url_for, request
from sqlalchemy.exc import IntegrityError

from startingbusiness_app import db
from startingbusiness_app.auth.forms import SignupForm, LoginForm
from startingbusiness_app.models import User

auth_bp = Blueprint('auth', __name__, template_folder="templates")


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, account_type = form.account_type.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Hello {user.first_name} {user.last_name}, your registration was successful!", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register {form.email.data}. ', 'error')
            return redirect(url_for('auth.signup'))
        return redirect(url_for('main.index'))
    return render_template('auth/signup.html', title='Sign Up', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash(f"You are logged in as {login_form.email.data}")
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Login', form=login_form)