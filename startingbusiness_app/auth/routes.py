from flask import Blueprint, render_template, flash, redirect, url_for, request
from sqlalchemy.exc import IntegrityError
from startingbusiness_app import db, mail, photos
from startingbusiness_app.auth.forms import SignupForm, LoginForm, ResetPasswordRequestForm, ResetPasswordForm, \
    UpdateProfileForm
from startingbusiness_app.models import User
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from werkzeug.security import generate_password_hash
from PIL import Image
from pathlib import Path

auth_bp = Blueprint('auth', __name__, template_folder="templates")


def send_registration_email(user):
    message = Message('Starting a Business App - Registration Confirmation', recipients=[user.email])
    message.body = f'''Hello {user.first_name},
thank you for registering for a {user.account_type} account on Starting a Business App. 

The application offers a wide range of functionalities such as:
- regional and global comparison of indicators to start a business 
- gender analysis tools
- blogs for discussion  

We hope you enjoy your use of the app,
the StartingABusiness Team.
'''
    mail.send(message)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate_on_submit():
        filename = "default.jpg"
        if 'photo' in request.files:
            if request.files['photo'].filename!= '':
                request.files['photo'].filename = generate_password_hash(request.files['photo'].filename) + '.jpg'
                filename = photos.save(request.files['photo'])
                image_path = Path(__file__).parent
                image_path2 = image_path.parent.joinpath("static/profile_images")
                temp_image = Image.open(str(image_path2) + '/'+filename)
                temp_image.thumbnail((400,400))
                temp_image.save(str(image_path2) + '/'+filename)
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                    account_type=form.account_type.data, profile_image=filename)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            send_registration_email(user)
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
        if request.method == 'POST' and update_form.validate_on_submit():
            filename = current_user.profile_image
            if 'photo' in request.files:
                if request.files['photo'].filename != '':
                    request.files['photo'].filename = generate_password_hash(request.files['photo'].filename) + '.jpg'
                    filename = photos.save(request.files['photo'])
                    image_path = Path(__file__).parent
                    image_path2 = image_path.parent.joinpath("static/profile_images")
                    temp_image = Image.open(str(image_path2) + '/' + filename)
                    temp_image.thumbnail((400, 400))
                    temp_image.save(str(image_path2) + '/' + filename)
        current_user.profile_image = filename
        try:
            db.session.commit()
            flash(
                f"Hello {update_form.first_name.data} {update_form.last_name.data}, your profile was updated successfully!",
                'success')
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to update {update_form.email.data} account.', 'error')
            return redirect(url_for('auth.profile'))
    elif request.method == 'GET':
        update_form.first_name.data = current_user.first_name
        update_form.last_name.data = current_user.last_name
        update_form.email.data = current_user.email
        update_form.account_type.data = current_user.account_type

    return render_template('auth/profile.html', title='Profile', form=update_form, image_file= current_user.profile_image)


def send_reset_email(user):
    # flash('Check your inbox for an email with password reset instructions', 'info')
    tok = user.get_token()
    message = Message('Starting a Business App - Password Reset', recipients=[user.email])
    message.body = f'''Hello {user.first_name},
we have received a password reset request.
    
To reset your password click on the link: {url_for('auth.password_reset', token=tok, _external=True)}

If you were not the one who made this request, please ignore this email. 
    '''
    mail.send(message)


@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def password_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    reset_pw_request_form = ResetPasswordRequestForm()
    if reset_pw_request_form.validate_on_submit():
        user = User.query.filter_by(email=reset_pw_request_form.email.data).first()
        send_reset_email(user)
        flash('Check your inbox for an email with password reset instructions', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/password_request.html', title='Request Reset Password', form=reset_pw_request_form)


@auth_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    user = User.verify_token(token)
    if not user:
        flash('The password reset link is invalid', 'warning')
        return redirect(url_for('auth.password_request'))
    reset_pw_token_form = ResetPasswordForm()
    if reset_pw_token_form.validate_on_submit():
        user.set_password(reset_pw_token_form.password.data)
        try:
            db.session.commit()
            flash(f"Hello {user.first_name} {user.last_name}, your password was reset!", 'success')
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to reset password.', 'error')
            return redirect(url_for('auth.password_request'))
        return redirect(url_for('auth.login'))
    return render_template('auth/password_reset.html', title='Reset Password', form=reset_pw_token_form)
