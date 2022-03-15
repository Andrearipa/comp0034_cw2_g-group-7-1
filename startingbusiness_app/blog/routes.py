"""
This file was developed to establish the routes for the blog blueprint.
"""

from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_required, current_user
from flask_mail import Message
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError
from startingbusiness_app import db, mail
from startingbusiness_app.blog.forms import CreateNewPost, ModifyPost, Post, BlogPage
from startingbusiness_app.models import Blog, User

blog_bp = Blueprint('blog', __name__, template_folder='templates', static_folder='static')


@blog_bp.route('', methods=['GET', 'POST'])
def blog():
    posts = Blog.query.order_by(Blog.date_posted.desc()).all()
    blog_form = BlogPage()
    word = blog_form.filter_keyword.data
    if blog_form.validate_on_submit():
        if word:
            posts = Blog.query.filter(or_(Blog.title.contains(word), Blog.content.contains(word))).order_by(
                Blog.date_posted.desc())
            blog_form.filter_keyword.data = ""
            flash(f"Posts filtered by '{word}'", "info")
            return render_template('blog/blog.html', form=blog_form, posts=posts, title='Blog')
        elif blog_form.add_post_button:
            return redirect(url_for('blog.new_post'))
    return render_template('blog/blog.html', form=blog_form, posts=posts, title='Blog')


def send_post_email(user, post_email):
    message = Message('Starting a Business App - New Post', recipients=[user.email])
    message.body = f'''Hello {user.first_name},
thank you for adding a new post to the blog!

Here is your post:
    TITLE: {post_email.title}
    
    MAIN BODY:
    {post_email.content}
'''
    mail.send(message)


@blog_bp.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    post_form = CreateNewPost()
    if post_form.validate_on_submit():
        new_post_action = Blog(title=post_form.title.data, content=post_form.content.data, author=current_user)
        try:
            db.session.add(new_post_action)
            db.session.commit()
            send_post_email(current_user, new_post_action)
            flash('Your post has been published successfully', 'success')
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to publish the post.', 'error')
        return redirect(url_for('blog.blog'))
    return render_template('blog/create_update_post.html', form=post_form, title='New Post')


@blog_bp.route("/post/<int:post_id>")
def post(post_id):
    post_form = Post()
    single_post = Blog.query.get_or_404(post_id)
    return render_template('blog/post.html', title=single_post.title, post=single_post, form=post_form)


@blog_bp.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def modify_post(post_id):
    modify_post_action = Blog.query.get_or_404(post_id)
    if modify_post_action.author != current_user:
        abort(403)
    post_form = ModifyPost()
    if post_form.validate_on_submit():
        modify_post_action.title = post_form.title.data
        modify_post_action.content = post_form.content.data
        try:
            db.session.add(modify_post_action)
            db.session.commit()
            flash('Your post has been updated successfully', 'success')
        except IntegrityError:
            db.session.rollback()
            flash(f'Error, unable to update the post.', 'error')
        return redirect(url_for('blog.post', post_id=modify_post_action.id))
    elif request.method == 'GET':
        post_form.title.data = modify_post_action.title
        post_form.content.data = modify_post_action.content
    return render_template('blog/create_update_post.html', title='Update Post', form=post_form, legend='Update Post')


@blog_bp.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    delete_post_action = Blog.query.get_or_404(post_id)
    post_form = BlogPage()
    if delete_post_action.author != current_user:
        abort(403)
    try:
        db.session.delete(delete_post_action)
        db.session.commit()
        flash('Your post has been deleted!', 'success')
        redirect(url_for('blog.blog'))
    except IntegrityError:
        db.session.rollback()
        flash(f'Error, unable to delete the post.', 'error')
    posts = Blog.query.order_by(Blog.date_posted.desc()).all()
    return render_template('blog/blog.html', title='Update Post', form=post_form, posts=posts, legend='Update Post')


@blog_bp.route("/user/<string:email>")
def user_posts(email):
    user = User.query.filter_by(email=email).first_or_404()
    posts = Blog.query.filter_by(author=user).order_by(Blog.date_posted.desc())
    blog_form = BlogPage()
    return render_template('blog/blog.html', form=blog_form, posts=posts, user=user)
