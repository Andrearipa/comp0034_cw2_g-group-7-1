# Response Links https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#redirection_messages
from flask_login import login_user, current_user
from startingbusiness_app.models import User
from werkzeug.security import generate_password_hash


def register_user(client, user_info):
    """ Given a Registration Form, Registers a new user"""
    return client.post('/signup', data = user_info, follow_redirects=True)


def login(client, email, password):
    """Provides login to be used in tests"""
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


def submit_password_request(client, email):
    """Submits a password request form"""
    return client.post('/reset_password', data=dict(email=email), follow_redirects=True)


def submit_password_reset(client, link, password):
    """ Sends a password change """
    return client.post(link, data=dict(password=password, password_repeat=password), follow_redirects=True)


def profile_change(client, email):
    """ Changes the profile """
    photo_path = 'startingbusiness_app/static/profile_images/Default.jpg'
    return client.post('/profile',
                       data=dict(first_name='Default', last_name='Default', email=email, account_type='Entrepreneur', photo=photo_path),
                       follow_redirects=True)

def test_au01_registration_correct(test_client, db):
    """
    GIVEN a user is not registered
    WHEN they submit a valid registration form
    THEN they are redirected to the home page
        AND a successful registration messaged is flashed
        AND the new account is added to the database
    """
    start_users = User.query.count()
    if current_user:
        test_client.get('/logout')

    new_user = dict(first_name='Caterina', last_name='Rossi', email='testnewuser@test.1',
                    password='CiaoCiao', password_repeat ='CiaoCiao', account_type='Student')
    response = register_user(test_client, new_user)
    end_users = User.query.count()
    assert b'administrator' in response.data
    assert b'Hello Caterina Rossi, your registration was successful!' in response.data
    assert end_users - start_users == 1


def test_au02_registration_repeated_email(test_client, db):
    """
    GIVEN a user is not registered
    WHEN they submit a registration form with an email that is already taken
    THEN they are redirected to the registration page
        AND an error message appears below the email field
        AND their account is not added to the database
    """
    start_users = User.query.count()
    if current_user:
        test_client.get('/logout')

    new_user = dict(first_name='Caterina', last_name='Rossi', email='kate.vanelli@gmail.com',
                    password='CiaoCiao', password_repeat='CiaoCiao', account_type='Student')
    response = register_user(test_client, new_user)
    end_users = User.query.count()
    assert b'Register with us !' in response.data
    assert b'An account is already registered with this email address' in response.data
    assert end_users - start_users == 0


def test_au03_registration_different_passwords(test_client, db):
    """
    GIVEN a user is not registered
    WHEN they submit a registration form in which the two passwords don't match (case sensitive)
    THEN they are redirected to the registration page
        AND an error message appears below the repeat password field
        AND their account is not added to the database
    """
    start_users = User.query.count()
    if current_user:
        test_client.get('/logout')

    new_user = dict(first_name='Caterina', last_name='Rossi', email='testnewuser@test.1',
                    password='Ciaociao', password_repeat='CiaoCiao', account_type='Student')
    response = register_user(test_client, new_user)
    end_users = User.query.count()
    assert b'Register with us !' in response.data
    assert b'Passwords must match' in response.data
    assert end_users - start_users == 0


def test_au06_login_correct(test_client, db):
    """
    GIVEN a user is registered
    WHEN they submit a valid login form (i.e. correct email and password)
    THEN they are redirected to the home page
        AND a successful login messaged is flashed
        AND the 'Profile' and 'Log Out' functionalities are available
    """
    if current_user:
        test_client.get('/logout')

    response = login(test_client, email='kate.vanelli@gmail.com', password='Hello456')
    assert response.status_code == 200
    assert current_user.is_authenticated
    assert b'administrator' in response.data
    assert b'You are logged in as kate.vanelli@gmail.com' in response.data
    assert b'Profile' in response.data
    assert b'Log out' in response.data



def test_au07_login_incorrect(test_client, db):
    """
    GIVEN a user is registered
    WHEN they submit an invalid login form (i.e. incorrect password for correct email)
    THEN they are redirected to the login page
        AND an error message is displayed under the password field
        AND they cannot access the Profile and Log Out functionalities
    """
    if current_user:
        test_client.get('/logout')

    response = login(test_client, email='kate.vanelli@gmail.com', password='Hello')
    assert response.status_code == 200
    assert not current_user.is_authenticated
    assert b'Incorrect password' in response.data
    assert b'Log in!' in response.data
    assert b'Profile' not in response.data
    assert b'Log out' not in response.data


def test_au08_password_reset(test_client, db):
    """
    GIVEN a user is registered
    WHEN they request a password reset from the login page
    THEN a token is generated
        AND the page /reset_password/<token> shows a reset password form
        AND WHEN the user submits a correct form
            THEN the new password is correctly associated with their account
    """
    new_user = User(first_name='Andrea', last_name='Ripa', email='testnewuser@test.1', password=generate_password_hash("Italy123"),
                      account_type='Student')
    db.session.add(new_user)
    db.session.commit()
    if current_user:
        test_client.get('/logout')

    response = submit_password_request(test_client, 'testnewuser@test.1')
    assert b'Check your inbox for an email with password reset instructions' in response.data

    token = new_user.get_token()
    link = '/reset_password/' + str(token)
    request_response = test_client.get(link)

    assert request_response.status_code == 200
    assert b' Reset your password ' in request_response.data

    reset_response = submit_password_reset(test_client, link, 'ThisIsANewPassword')

    assert b'Log in!' in reset_response.data

    login_response = login(test_client, 'testnewuser@test.1', 'ThisIsANewPassword')
    assert login_response.status_code == 200
    assert current_user.is_authenticated
    assert b'administrator' in login_response.data


def test_au09_change_email(test_client, db):
    """
    GIVEN a user is registered
    WHEN they submit a profile change form to modify their email
    THEN the email stored for their account is correctly modified
    """

    login(test_client, email='danielle_konig@123.co.uk', password='Canada789')

    profile_response = profile_change(test_client, 'danielle_konig@789.co.uk')

    assert b'your profile was updated successfully!' in profile_response.data
    response = login(test_client, email='danielle_konig@789.co.uk', password='Canada789')
    assert b'Profile' in response.data
    assert b'Log out' in response.data


def test_au10_logout(test_client, db):
    """
    GIVEN a user is logged in
    WHEN they submit a logout request
    THEN the current user becomes null
    """
    if not current_user:
        login(test_client, email='danielle_konig@123.co.uk', password='Canada789')

    test_client.get('/logout')

    assert not current_user.is_authenticated


