"""
This file is used to test the different components linked to the blog blueprint, to check whether they are working
together properly. Especially the tests focus on the functionality that the user will be using and the required
interactions. These are mainly two and are with the flask application routes and the database.
"""
from flask_login import current_user
from startingbusiness_app.models import Blog


def login(client, email, password):
    """Provides login to be used in tests"""
    return client.post('/login', data=dict(email=email, password=password), follow_redirects=True)


def blog(client):
    """Provides blog to be used in tests"""
    return client.get('/blog')


def create_post_access(client):
    """Provides create post to be used in tests"""
    return client.get('/blog/post/new')


def create_post_publish(client, title, content):
    """Provides create post to be used in tests"""
    return client.post('/blog/post/new', data=dict(title=title, content=content), follow_redirects=True)


def test_bl01_guest_access_blog(test_client, db):
    """
    GIVEN that the app is running and user is not logged in
    WHEN they try to access the blog
    THEN they should be able to see the posts (find the word Italy)
    """
    response = blog(test_client)
    assert response.status_code == 200
    assert b'Italy' in response.data


def test_bl02_logged_user_access_blog(test_client, db):
    """
    GIVEN that the app is running and user is logged in
    WHEN they try to access the blog
    THEN they should be able to see the posts
    """
    login(test_client, email='kate.vanelli@gmail.com', password='Hello456')
    response = blog(test_client)
    assert response.status_code == 200
    assert current_user.is_authenticated, 'Login failed'
    assert b'Italy' in response.data, 'Blog is not displayed'
    test_client.get('/logout')


def test_bl03_guest_create_post(test_client, db):
    """
    GIVEN that the app is running and user is not logged in
    WHEN they try to access the blog and create a post
    THEN they should not be able to create a post and be redirected to log in
    """
    response_1 = create_post_access(test_client)
    assert response_1.status_code == 302
    response_2 = test_client.get('/blog/post/new', follow_redirects=True)
    assert b'Please log in to access this page' in response_2.data, 'Guest is not redirected to login page'


def test_bl04_logged_user_create_post(test_client, db):
    """
    GIVEN that the app is running and user is logged in
    WHEN they try to access the blog and create a post
    THEN they should be able to create and post it on the blog
    """
    login(test_client, email='kate.vanelli@gmail.com', password='Hello456')
    response_access = create_post_access(test_client)
    assert response_access.status_code == 200
    assert b'Create Post' in response_access.data, 'Create post page is not accessed'
    response_pub = create_post_publish(test_client, title='Test post 4', content='This is the content for test_bl04')
    assert response_pub.status_code == 200
    assert b'Your post has been published successfully' in response_pub.data, 'No flash message displayed'
    assert b'test_bl04' in response_pub.data, 'Post has not been published'
    test_client.get('/logout')


def test_bl05_search_post_keyword(test_client, db):
    """
    GIVEN that the user has accessed the blog
    WHEN they try to search for a post by keyword
    THEN a list of the matching posts should be return
    """
    response = test_client.post('/blog', data=dict(filter_keyword='Italy'), follow_redirects=True)
    assert response.status_code == 200
    assert b'Posts filtered by' in response.data, 'No flash message displayed after filtering'
    assert b'Test Post 2' not in response.data, 'Filtering did not work'


def test_bl06_filter_posts_by_author(test_client, db):
    """
    GIVEN that the user has accessed the blog
    WHEN they try to filter the posts by the author
    THEN a list of the matching posts should be return
    """
    response = test_client.get('/blog/user/kate.vanelli@gmail.com')
    assert response.status_code == 200
    assert b'andrearipa4@gmail.com' not in response.data


def test_bl07_guest_access_single_post(test_client):
    """
    GIVEN that the user is not logged in or simply not the post author
    WHEN they access a single post created by another user
    THEN the post should be the only one displayed and no option to update (or delete) should be available
    """
    login(test_client, email='kate.vanelli@gmail.com', password='Hello456')
    response = test_client.get('/blog/post/1')
    assert response.status_code == 200
    assert b'Italy' not in response.data, 'Single post has not been accessed'
    assert b'Update' not in response.data, 'Update option available to user that is not the author of post'
    test_client.get('/logout')


def test_bl08_user_access_own_single_post(test_client, db):
    """
    GIVEN that the user is logged in
    WHEN they access their own post
    THEN the post should be the only one displayed and the option to update (or delete) should be available
    """
    login(test_client, email='kate.vanelli@gmail.com', password='Hello456')
    response_1 = test_client.get('/blog/post/2')
    assert response_1.status_code == 200
    assert b'andrearipa4@gmail.com' not in response_1.data, 'Single post has not been accessed'
    assert b'Update' in response_1.data, 'Update option not available to user that is the author of post'
    response_2 = test_client.get('blog/post/1/update')
    assert response_2.status_code == 403, 'Update page should be forbidden to non author'
    test_client.get('/logout')


def test_bl09_update_post(test_client, db):
    """
    GIVEN that the user is logged in
    WHEN they access their own post and try to update it
    THEN they should be able to update it and submit it
    """
    login(test_client, email='kate.vanelli@gmail.com', password='Hello456')
    response_pre_upd = blog(test_client)
    assert response_pre_upd.status_code == 200
    assert b'Italy' in response_pre_upd.data, 'Blog is not displayed'
    response_post_upd = test_client.post('blog/post/3/update',
                                         data=dict(title='Test post 3 update',
                                                   content='Interesting business score for Germany in 2017'),
                                         follow_redirects=True)
    assert response_post_upd.status_code == 200
    assert b'Your post has been updated successfully' in response_post_upd.data, 'No flash message displayed after update'
    assert b'Germany' in response_post_upd.data, 'Blog is not displayed updated'
    test_client.get('/logout')


def test_bl10_delete_post(test_client, db):
    """
    GIVEN that the user is logged in
    WHEN they access their own post
    THEN they should be able to permanently delete their post
    """
    login(test_client, email='kate.vanelli@gmail.com', password='Hello456')
    response_pre_del = blog(test_client)
    num_of_post_pre_del = Blog.query.count()
    assert response_pre_del.status_code == 200
    assert b'Italy' in response_pre_del.data, 'Blog is not displayed'
    response_post_del = test_client.post('blog/post/3/delete', follow_redirects=True)
    num_of_post_post_del = Blog.query.count()
    assert response_post_del.status_code == 200
    assert b'Your post has been deleted!' in response_post_del.data
    assert num_of_post_pre_del - num_of_post_post_del == 1
    test_client.get('/logout')

