from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import CSRFProtect

db = SQLAlchemy()
photos = UploadSet('photos', IMAGES)
mail = Mail()
login_manager = LoginManager()
csrf = CSRFProtect()
csrf._exempt_views.add('dash.dash.dispatch')


def create_app(config_class_name):
    """
    Initialise the Flask application.
    :type config_class_name: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """

    app = Flask(__name__)

    app.config.from_object(config_class_name)
    # register_dashapp(app)
    from startingbusiness_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)
    from startingbusiness_app.main.routes import main_bp
    app.register_blueprint(main_bp)
    from startingbusiness_app.blog.routes import blog_bp
    app.register_blueprint(blog_bp, url_prefix='/blog')

    app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'startingabusiness.app@gmail.com'
    app.config['MAIL_PASSWORD'] = 'ewlvlhmlkhwhqvni'
    app.config['MAIL_DEFAULT_SENDER'] = 'noreply@sbapp.com'

    db.init_app(app)
    configure_uploads(app, photos)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    csrf.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from app_cm.Choropleth_app import init_dashboard
        app = init_dashboard(app)

    with app.app_context():
        from startingbusiness_app.models import User, Blog
        db.create_all()

    with app.app_context():
        from Bubble_Chart.Bubble_Chart_app import init_dashboard
        app = init_dashboard(app)

    return app
