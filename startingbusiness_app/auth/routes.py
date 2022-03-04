from flask import Blueprint, render_template, flash, redirect, url_for, request
from sqlalchemy.exc import IntegrityError

from startingbusiness_app import db
from startingbusiness_app.auth.forms import SignupForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm
from startingbusiness_app.models import User
from flask_login import current_user
from flask_mail import Message
from startingbusiness_app.app import mail

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
            flash(f'Error, unable to register {form.email.data}.', 'error')
            return redirect(url_for('auth.signup'))
        return redirect(url_for('main.index'))
    return render_template('auth/signup.html', title='Sign Up', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        flash(f"You are logged in as {login_form.email.data}", 'success')
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Login', form=login_form)


def send_reset_email(user):
    token = user.get_token()
    message = Message('Password Reset Email', sender='noreply@demo.com', recipients=[user.email])
    message.body = f'''To reset your password click on the link: {url_for('reset_pw_token', token = token, _external=True)}

If the request was not made by you, please ignore this email
    '''
    pass


@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_pw_request():
    '''if current_user.is_authenticated:
        return redirect(url_for('home'))'''
    reset_pw_request_form = ResetPasswordRequestForm()
    if reset_pw_request_form.validate_on_submit():
        user = User.query.filter_by(email=reset_pw_request_form.email.data).first()
        send_reset_email(user)
        flash('Check your inbox for an email with password reset instructions', 'info')
        return redirect(url_for('login'))
    return render_template('auth/password_request.html', title='Request Reset Password', form=reset_pw_request_form)


@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_pw_token(token):
    '''if current_user.is_authenticated:
        return redirect(url_for('home'))'''

    user = User.verify_token(token)
    if not user:
        flash('The password reset link is invalid', 'warning')
        return redirect(url_for('reset_pw_request'))
    reset_pw_token_form = ResetPasswordRequestForm()

    '''if reset_pw_request_form.validate_on_submit():
        user = User.query.filter_by(email=reset_pw_request_form.email.data).first()
        send_reset_email(user)
        flash('Check your inbox for an email with password reset instructions', 'info')
        return redirect(url_for('#'))'''
    return render_template('auth/password_reset.html', title='Reset Password', form=reset_pw_token_form)


