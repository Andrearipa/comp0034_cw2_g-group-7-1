from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from sqlalchemy.exc import IntegrityError

from startingbusiness_app import db
from startingbusiness_app.auth.forms import SignupForm, LoginForm
from startingbusiness_app.models import Blog
from flask_login import login_required, current_user
from startingbusiness_app.blog.forms import CreateNewPost

blog_bp = Blueprint('blog', __name__, template_folder='templates', static_folder='static')


@blog_bp.route('')
def blog():
    posts = Blog.query.all()
    return render_template('blog/blog.html', posts=posts, title='Blog')


@blog_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    post_form = CreateNewPost()
    if post_form.validate_on_submit():
        new_post = Blog(title=post_form.title.data, content=post_form.content.data, author=current_user)
        try:
            db.session.add(new_post)
            db.session.commit()
            flash('Your post has been published successfully', 'success')
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to publish the post.', 'error')
        return redirect(url_for('blog.blog'))
    return render_template('blog/create_update_post.html', form=post_form, title='New Post')


@blog_bp.route("/post/<int:post_id>")
def post(post_id):
    single_post = Blog.query.get_or_404(post_id)
    return render_template('blog/post.html', title=single_post.title, post=single_post)


@blog_bp.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def modify_post(post_id):
    change_post = Blog.query.get_or_404(post_id)
    if change_post.author != current_user:
        abort(403)
    post_form = CreateNewPost()
    if post_form.validate_on_submit():
        change_post.title = post_form.title.data
        change_post.content = post_form.content.data
        try:
            db.session.add(change_post)
            db.session.commit()
            flash('Your post has been updated successfully', 'success')
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to update the post.', 'error')
        return redirect(url_for('blog.post', post_id=change_post.id))
    elif request.method == 'GET':
        post_form.title.data = change_post.title
        post_form.content.data = change_post.content
    return render_template('blog/create_update_post.html', title='Update Post', form=post_form, legend='Update Post')


@blog_bp.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    delete_post = Blog.query.get_or_404(post_id)
    if delete_post.author != current_user:
        abort(403)
    try:
        db.session.delete(delete_post)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
    except IntegrityError:
        db.session.rollback()
        flash(f'Error, unable to delete the post.', 'error')
    return redirect(url_for('blog.blog'))

