import pytest
from startingbusiness_app import create_app, config
from startingbusiness_app.models import db as database, User, Blog
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='session')
def app():
    """
    Create an app to be used for testing.

    :return: app created for testing config
    """
    app = create_app(config_class_name=config.TestingConfig)
    yield app


@pytest.fixture(scope='session')
def test_client(app):
    """
    Create a test client that can be used to make HTTP requests and other actions.

    :param app: fixture to create the app
    :return: client for testing
    """
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='session')
def db(app):
    """
    Returns a database used for testing purposes with added values for both the user and blog table.

    :param app: fixture to create the app
    :return: database with user and blog values
    """
    with app.app_context():
        database.app = app
        database.create_all()
        user_1 = User(first_name='Andrea', last_name='Ripa', email='andrearipa4@gmail.com',
                      password=generate_password_hash("Italy123"),
                      account_type='Student')
        user_2 = User(first_name='Caterina', last_name='Vanelli Coralli', email='kate.vanelli@gmail.com',
                      password=generate_password_hash('Hello456'), account_type='Professional')
        user_3 = User(first_name='Danielle', last_name='Konig', email='danielle_konig@123.co.uk',
                      password=generate_password_hash('Canada789'),
                      account_type='Entrepreneur',
                      profile_image='startingbusiness_app/static/profile_images/Default.jpg')

        user_1.posts.append(Blog(title='Test Post 1', content='Content for test post 1 by user 1'))
        user_2.posts.append(Blog(title='Test Post 2', content='Content for test post 2 by user 2'))
        user_2.posts.append(Blog(title='Test Post 3', content='Interesting business score for Italy in 2017'))

        database.session.add(user_1)
        database.session.add(user_2)
        database.session.add(user_3)
        database.session.commit()

    yield database
    database.drop_all()


@pytest.fixture(scope='function', autouse=True)
def session(db, app):
    """
    Roll back database changes at the end of each test.

    :param db: database defined for session scope with user and blog for testing
    :param app: app running for testing config
    :return: None
    """
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        options = dict(bind=connection, binds={})
        sess = db.create_scoped_session(options=options)
        db.session = sess
        yield sess
        sess.remove()
        transaction.rollback()
        connection.close()
