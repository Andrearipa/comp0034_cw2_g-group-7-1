from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_class_name):
    """
    Initialise the Flask application.
    :type config_class_name: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class_name)
    '''from startingbusiness_app.auth.routes import auth_bp
    from startingbusiness_app.main.routes import main_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)'''

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from app_cm.Choropleth_app import init_dashboard
        app = init_dashboard(app)

    return app
