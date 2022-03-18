from startingbusiness_app.models import User
from startingbusiness_app.models import Blog
from datetime import date

user_data = {
    'first_name': 'Andrea',
    'last_name': 'Ripa',
    'password': 'Italy123',
    'email': 'andrearipa4@gmail.com',
    'account_type': 'Student'
}


def test_mo01_new_user():
    """
    GIVEN a User model
    WHEN a new user is created
    THEN check the first_name, last_name, email, and account_type fields are defined correctly
    """
    user = User(first_name=user_data['first_name'], last_name=user_data['last_name'], email=user_data['email'],
                account_type=user_data['account_type'])

    assert user.first_name == 'Andrea'
    assert user.last_name == 'Ripa'
    assert user.email == 'andrearipa4@gmail.com'
    assert user.account_type == 'Student'


def test_mo02_password_hashing():
    """
    GIVEN a User password
    WHEN a password is defined
    THEN check whether the password has been hashed
    """
    user = User(password=user_data['password'])
    assert user.check_password(user.password) != 'Italy123'


def test_mo03_new_blog_post():
    """
    GIVEN a Blog model
    WHEN a new blog is created
    THEN check the title, date_posted, and content fields are entered defined correctly
    """
    blog_data = {
        'title': 'Test Post',
        'date_posted': date.today(),
        'content': 'Content from Test Post',
    }

    blog = Blog(title=blog_data['title'], date_posted=blog_data['date_posted'], content=blog_data['content'])

    assert blog.title == 'Test Post'
    assert blog.date_posted == date.today()
    assert blog.content == 'Content from Test Post'
