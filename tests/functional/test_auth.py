# Response Links https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#redirection_messages


def test_au01_accessibility_if_logged_in():
    """
    GIVEN the app is running
    WHEN a user is logged in
    THEN the 'Profile' and 'Log Out' functionalities are available
        AND the Login link is not viewable
    """
    pass


def test_au02_accessibility_if_not_logged_in():
    """
    GIVEN the app is running
    WHEN a user is not logged in
    THEN they cannot access the Profile and Log Out functionalities
         AND the Login link is viewable
    """
    pass


def test_au03_registration_correct():
    """
    GIVEN a user is not registered
    WHEN they submit a valid registration form
    THEN they are redirected to the home page
        AND a successful registration messaged is flashed
        AND the new account is added to the database
    """
    pass


def test_au04_registration_repeated_email():
    """
    GIVEN a user is not registered
    WHEN they submit a registration form with an email that is already taken
    THEN they are redirected to the registration page
        AND an error message appears below the email field
        AND their account is not added to the database
    """
    pass


def test_au05_registration_different_passwords():
    """
    GIVEN a user is not registered
    WHEN they submit a registration form in which the two passwords don't match
    THEN they are redirected to the registration page
        AND an error message appears below the repeat password field
        AND their account is not added to the database
    """
    pass


def test_au06_login_correct():
    """
    GIVEN a user is registered
    WHEN they submit a valid login form (i.e. correct email and password)
    THEN they are redirected to the home page
        AND a successful login messaged is flashed
    """
    pass


def test_au07_login_incorrect():
    """
    GIVEN a user is registered
    WHEN they submit an invalid login form (i.e. incorrect password for correct email)
    THEN they are redirected to the login page
        AND an error message is displayed under the password field
    """
    pass


def test_au08_password_reset():
    """
    GIVEN a user is registered
    WHEN they request a password reset from the login page
    THEN a token is generated
        AND the page /reset_password/<token> shows a reset password form
        AND WHEN the user submits a correct form
            THEN the new password is correctly associated with their account
    """
    pass


def test_au09_change_email():
    """
    GIVEN a user is registered
    WHEN they submit a profile change form to modify their email
    THEN the email stored for their account is correctly modified
    """
    pass


def test_au10_logout():
    """
    GIVEN a user is logged in
    WHEN they submit a logout request
    THEN the current user becomes null
    """
    pass



