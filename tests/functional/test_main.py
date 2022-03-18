"""
This file is used to test the different components linked to the main blueprint, to check whether they are working
together properly. Especially the tests focus on the functionality that the user will be using and the required
interactions. These are mainly two and are with the flask application routes and the database.
"""
import pytest
from flask_login import current_user


def login(client, email, password):
    """
    Provides login to be used in tests.

    :param client: test_client
    :param email: user email
    :param password: user password
    :return: http response
    """
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


def test_ma01_homepage_valid(test_client):
    """
    GIVEN: that the app is running
    WHEN: the user is on the home page
    THEN: the footer should be displayed
    """
    response = test_client.get('/home')
    assert response.status_code == 200
    assert b'IFP' in response.data, 'Footer not displayed'


def test_ma02_homepage_content(test_client):
    """
    GIVEN: that the app is running
    WHEN: the user is on the home page
    THEN: the navbar should display log in
    """
    response = test_client.get('/home')
    assert b'Log In!' not in response.data, 'Incorrect page is displayed'
    assert b'Choropleth Map' in response.data, 'Navbar not displayed'


def test_ma03_home_page_content_header(test_client):
    """
    GIVEN: that the app is running
    WHEN: it is in the main page
    THEN: starting a business should be an h1 title
    """
    response = test_client.get('/home')
    assert b'<h1>Starting a Business</h1>' in response.data, 'Incorrect Page Displayed'


def test_ma05_blog_page_content(test_client):
    """
    GIVEN: that the app is running
    WHEN: the user is on the blog page
    THEN: the write a new post button should be displayed
    """
    response = test_client.get('/blog')
    assert b'Write a New Post' in response.data, 'Incorrect Page Displayed'


def test_ma06_sign_up_page_content(test_client):
    """
    GIVEN: that the app is running
    WHEN: the user is on the sign-up page
    THEN: the register with us message should be displayed
    """
    response = test_client.get('/signup')
    assert b'<b> Register with us ! </b>' in response.data, 'Incorrect Page Displayed'


def test_ma07_login_page_content(test_client):
    """
    GIVEN: that the app is running
    WHEN: the user is on the log in page
    THEN: the log in message should be displayed
    """
    response = test_client.get('/login')
    assert b'<b> Log in! </b>' in response.data, 'Incorrect Page Displayed'






