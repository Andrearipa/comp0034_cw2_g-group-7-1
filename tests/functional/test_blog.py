"""
This is the conftest.py file created on the 10/03/2022 for testing purposes.
"""
from startingbusiness_app.models import User


def login(client, email, password):
    """Provides login to be used in tests"""
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


def blog(client):
    """Provides login to be used in tests"""
    return client.get('/blog')


def test_user_login_success(test_client):
    """
    GIVEN a user with a valid username and password
    WHEN the user logs in
    THEN a HTTP 200 code is received
    """
    response = login(test_client, email='kate.vanelli@gmail.com', password='c')
    assert b'administrator' in response.data


def test_blog(test_client):
    """
    GIVEN a user with a valid username and password
    WHEN the user logs in
    THEN a HTTP 200 code is received
    """
    response = blog(test_client)
    assert b'pizza' in response.data
