from flask import Blueprint, render_template, flash, redirect, url_for, request
from sqlalchemy.exc import IntegrityError

from startingbusiness_app import db
from startingbusiness_app.auth.forms import SignupForm, LoginForm
from startingbusiness_app.models import User

blog_bp = Blueprint('blog', __name__, template_folder='templates', static_folder='static')

posts = [
    {
        'author': 'Andrea Ripa',
        'title': 'Blog Post 1',
        'content': 'Caterina cooks pancakes with Louis'
    },
    {
        'author': 'Caterina Vanelli',
        'title': 'Blog Post 2',
        'content': 'Andrea è proprio scemo, dentro intendo!!'
    }
]


@blog_bp.route('')
def blog():
    return render_template('blog/blog.html', posts=posts, title='Blog')

