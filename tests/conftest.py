import pytest
from startingbusiness_app import create_app, config
from startingbusiness_app.models import db as database, User, Blog
from werkzeug.security import generate_password_hash


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
        user_1 = User(first_name='Andrea', last_name='Ripa', email='andrearipa4@gmail.com', password=generate_password_hash("Italy123"),
                      account_type='Student')
        user_2 = User(first_name='Caterina', last_name='Vanelli Coralli', email='kate.vanelli@gmail.com',
                      password=generate_password_hash('Hello456'), account_type='Professional')
        user_3 = User(first_name='Danielle', last_name='Konig', email='danielle_konig@123.co.uk', password=generate_password_hash('Canada789'),
                      account_type='Entrepreneur')

        user_1.posts.append(Blog(title='Test Post 1', content='Content for test post 1 by user 1'))
        user_2.posts.append(Blog(title='Test Post 2', content='Content for test post 2 by user 2'))
        user_2.posts.append(Blog(title='Test Post 3', content='Interesting business score for italy in 2017'))

        database.session.add(user_1)
        database.session.add(user_2)
        database.session.add(user_3)
        database.session.commit()

    yield database
    database.drop_all()
