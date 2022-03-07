from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required 
from sqlalchemy.exc import IntegrityError
from startingbusiness_app import db
from startingbusiness_app.auth.forms import SignupForm, LoginForm, UpdateAccountForm
from startingbusiness_app.models import User
from startingbusiness_app.models import login_manager

auth_bp = Blueprint('auth', __name__, template_folder= "templates")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data, account_type=form.account_type.data, profile_image =form.profile_image.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Hello, {user.first_name} {user.last_name}. You are signed up.")
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
        login_user(User.query.filter_by(email=login_form.email.data).first(), remember=login_form.remember.data)
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', title='Login', form=login_form)

@auth_bp.route('/profile', methods=['GET', 'POST'])
#@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.profile_image.data:
            picture_file = save_picture(form.profile_image.data)
            current_user.profile_image = picture_file
        current_user.first_name = form.first_name.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.first_name.data = current_user.first_name
        form.email.data = current_user.email
    image_file = url_for('static', filename=current_user.profile_image)
    return render_template('auth/profile.html', title='Account',
                           image_file=image_file, form=form)


'''def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(models.root_path, 'static','user', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn'''