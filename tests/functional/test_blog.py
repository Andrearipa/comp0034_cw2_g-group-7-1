"""
This file is used to test the different components linked to the blog blueprint, to check whether they are working
together properly. Especially the tests focus on the functionality that the user will be using and the required
interactions. These are mainly two and are with the flask application routes and the database.
"""
from startingbusiness_app.models import User


def login(client, email, password):
    """Provides login to be used in tests"""
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


def blog(client):
    """Provides login to be used in tests"""
    return client.get('/blog')


def test_user_login_success(test_client, db):
    """
    GIVEN a user with a valid username and password
    WHEN the user logs in
    THEN a HTTP 200 code is received
    """
    response = login(test_client, email='kate.vanelli@gmail.com', password='Hello456')
    assert b'administrator' in response.data


def test_blog(test_client, db):
    """
    GIVEN a user with a valid username and password
    WHEN the user logs in
    THEN a HTTP 200 code is received
    """
    response = blog(test_client)
    assert b'pizza' in response.data


def test_bl01_guest_access_blog():
    """
    GIVEN that the app is running and user is not logged in
    WHEN they try to access the blog
    THEN they should be able to see the posts
    """
    pass


def test_bl02_logged_user_access_blog():
    """
    GIVEN that the app is running and user is logged in
    WHEN they try to access the blog
    THEN they should be able to see the posts
    """
    pass


def test_bl03_guest_create_post():
    """
    GIVEN that the app is running and user is not logged in
    WHEN they try to access the blog and create a post
    THEN they should not be able to create a post and be redirected to log in
    """
    pass


def test_bl04_logged_user_create_post():
    """
    GIVEN that the app is running and user is logged in
    WHEN they try to access the blog and create a post
    THEN they should nbe able to creat and post it on the blog
    """
    pass


def test_bl05_search_post_keyword():
    """
    GIVEN that the user has accessed the blog
    WHEN they try to search for a post by keyword
    THEN a list of the matching posts should be return
    """
    pass


def test_bl06_filter_posts_by_author():
    """
    GIVEN that the user has accessed the blog
    WHEN they try to filter the posts by the author
    THEN a list of the matching posts should be return
    """
    pass


def test_bl07_guest_access_single_post():
    """
    GIVEN that the user is not logged in or simply not the post author
    WHEN they access a single post created by another user
    THEN the post should be the only one displayed and no option to update or delete should be available
    """
    pass


def test_bl08_user_access_own_single_post():
    """
    GIVEN that the user is logged in
    WHEN they access their own post
    THEN the post should be the only one displayed and the option to update or delete should be available
    """
    pass


def test_bl09_update_post():
    """
    GIVEN that the user is logged in
    WHEN they access their own post and try to update it
    THEN they should be able to update it and submit it
    """
    pass


def test_bl10_delete_post():
    """
    GIVEN that the user is logged in
    WHEN they access their own post
    THEN they should be able to permanently delete their post
    """
    pass
