"""Flask config class."""
from pathlib import Path


class Config(object):
    """
    Key generated using:
        import secrets
        print(secrets.token_urlsafe(16))
    """
    DEBUG = False
    SECRET_KEY = 'n_MImT106bAHxxAn2eogow'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #DATA_PATH = Path('Data Set')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(Path(__file__).parent.joinpath('startingbusiness_app.sqlite'))
    TESTING = False
    #EXPLAIN_TEMPLATE_LOADING = True


class ProductionConfig(Config):
    ENV = 'production'
    pass


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_ECHO = True
