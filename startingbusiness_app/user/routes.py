import secrets
from PIL import Image
from pathlib import Path
from flask import Blueprint, render_template
from flask import render_template, url_for, flash, redirect, request
import os
from startingbusiness_app import db,models
from flask_login import login_user, current_user, logout_user, login_required

from startingbusiness_app.user.forms import UpdateAccountForm
from startingbusiness_app import login_manager
from startingbusiness_app.models import User
from startingbusiness_app.models import login_manager
from startingbusiness_app.auth.routes import login


user_bp = Blueprint('user', __name__, template_folder="templates")
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
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
    return render_template('user/profile.html', title='Account',
                           image_file=image_file, form=form)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(models.root_path, 'static','user', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn