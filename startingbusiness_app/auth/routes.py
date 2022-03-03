from flask import Blueprint, render_template, flash, redirect, url_for, request
from sqlalchemy.exc import IntegrityError

from startingbusiness_app import db
from startingbusiness_app.auth.forms import SignupForm, LoginForm, UpdateProfileForm
from startingbusiness_app.models import User
from flask_login import login_user, current_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__, template_folder="templates")


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = SignupForm(request.form)
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, account_type=form.account_type.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Hello {user.first_name} {user.last_name}, your registration was successful!", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to register {form.email.data}.', 'error')
            return redirect(url_for('auth.signup'))
        return redirect(url_for('main.index'))
    return render_template('auth/signup.html', title='Sign Up', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        login_user(user, remember=login_form.remember.data)
        flash(f"You are logged in as {login_form.email.data}", 'success')
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Login', form=login_form)


@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    update_form = UpdateProfileForm()
    if update_form.validate_on_submit():
        current_user.first_name = update_form.first_name.data
        current_user.last_name = update_form.last_name.data
        current_user.email = update_form.email.data
        current_user.account_type = update_form.account_type.data
        try:
            db.session.commit()
            flash(f"Hello {update_form.first_name.data} {update_form.last_name.data}, your profile was updated successfully!", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to update {update_form.email.data} account.', 'error')
            return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        update_form.first_name.data = current_user.first_name
        update_form.last_name.data = current_user.last_name
        update_form.email.data = current_user.email
        update_form.account_type.data = current_user.account_type
    return render_template('auth/profile.html', title='Profile', form=update_form)
