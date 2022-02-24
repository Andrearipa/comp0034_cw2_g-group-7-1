from flask import Blueprint

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/')
def index():
    return "This is the user section of the web app"
