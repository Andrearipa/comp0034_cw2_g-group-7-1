import pytest
from startingbusiness_app import create_app, config
from startingbusiness_app.models import db as database, User, Blog


@pytest.fixture(scope='session')
def app():
    " Create an app to be used for testing"
    app = create_app(config_class_name=config.TestingConfig)
    yield app


@pytest.fixture(scope='session')
def test_client(app):
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='session')
def db(app):
    with app.app_context():
        database.app = app
        database.create_all()
        user_1 = User(first_name='Andrea', last_name='Ripa', email='andrearipa4@gmail.com', password='Italy123',
                      account_type='Student')
        user_2 = User(first_name='Caterina', last_name='Vanelli Coralli', email='kate.vanelli@gmail.com',
                      password='Hello456', account_type='Professional')
        user_3 = User(first_name='Danielle', last_name='Konig', email='danielle_konig@123.co.uk', password='Canada789',
                      account_type='Entrepreneur')
        database.session.add(user_1)
        database.session.add(user_2)
        database.session.add(user_3)
        database.session.commit()
    yield database
    database.drop_all()
