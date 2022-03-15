"""
This file was developed to establish the routes for the main blueprint.
"""

from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/home')
def index():
    return render_template('index.html', title="Starting a Business")
