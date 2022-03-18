# COMP0034 - Group 7 - Coursework 2

Points to mention:

- Created blog (create, uodate and delete) - filter by title and user name
- account, profile and login/logout (links not available always)
- email integration for new posts published and reset password and registration (email sent from account cretaed)
- responsive design for computer and phone
- error handling of databse with try and except and for forms ecc.
- overall structure with blueprints, css (static) and templates (html)
- security (secrfet key, hashed password)
- linting and github actions

To do:

- custom error handling
- integration of charts (add bubble chart)

- Check routes for testing
- Change the config parameters (disable csrf and add a different database for testing)

- add standard picture when no custom profile pic is selected

Questions:

- how to add posts to the database

# Ideas for Testing

In models (within unit folder), test: - DILARA

- user
    - check that the user is correctly created
    - test hash password
    - check the get / decode token methods
- blog
    - check that a blog is correctly created

In routes (functional folder), we check interactions with the SQL database, such as: - ANDREA + CATE

- check that all the links / pages are valid
- check accessibility based on login status
- create a new user and then a new post and see if that is recorded on the database
- check what happens if emails are repeated
- check for password differences
- check for password updates
- check login functionality

- design a test that does signup
    - an incorrect signup -> controls that it no user is registered if there are errors in the signup form
    - a correct signup -> the person is added to a new line in the database
- design a test for login
    - incorrect first
    - correct
    - ask for password reset -> go to the link with generated token, reset the password, check that it has been reset
- check changes on profile
    - change one or more data and verify whether they have been changed in the database
- posts:
    - create -> check in database
    - delete -> check in database

In browser: - NIKOS

- checking headings, etc
- use the by css selector
- use waits

Have a test for complete interaction of user with webpage

# References

if we have been following a general guideline, insert the reference here if we have copied code specifically, we can
reference it within the py file itself -> to be done for the blog

--ignore=tests/unit --ignore=tests/component

## Introduction

The team decided to develop a web app to integrate the dashboard with more functionalities. The functionalities
developed are based on the requirements highlighted in the first part of the project (Term 1). The functionalities taken
in consideration were also classified based on the importance. This ranking was used to prioritize the features to be
developed considering the time and resource constraint. Based on the aforementioned information, the features that the
team chose to develop are:

- Sign-up
- Log in/out
- Profile
- Blog
- Email Integration
- Dash Integration

All the features were developed using a blueprint structure and specific templates (html) and static files for style 
(css).

### Sign-Up:

The sign-up was developed to allow the user to register to access some additional functionalities. It is important to
mention that since the beginning of the project the team has always agreed that the dashboard should have been
accessible to any user. For this reason the additional features were then developed differently based on whether the
user is a guest (not-registered) or has a profile. In this way the purpose of creating a platform to share information
about starting a business would be met.

The sign-up consists in a quick form to fill with info about first name, surname, email, password and type of use. In
addition, there is also the possibility of adding a profile picture. The password is hashed before storing it for
security purposes.

### Log In/Out:

This feature allows the user to log in and out of the web app based on whether they want to navigate as guests or
authenticated users. In addition, in case the user forgot his password, there is the possibility to ask for a password
reset.

### Profile:

The profile section is only available to authenticated users, and it allows to modify the personal information
previously inserted during the registration.

### Blog:

The blog can be accessed by any type of user. However, only authenticated user can access the 'write a post'
functionality. The blog has also a filtering system based on a keyword search in both the title and content. Moreover,
it allows for a sorting based on ascending or descending published date or for title in alphabetical order. Finally, the
user that creates a post can at any moment update or delete it. The deletion process requires two steps to avoid
deletion made by mistake.

### Email Integration:

The email integration feature was developed and integrated with the sign-up, blog and password reset functionalities.
Firstly, when a new user is registered a confirmation email will be sent from the startingabusiness@gmail.com account.
Secondly, when a user adds a new post on the blog an email with the content is sent for confirmation. Finally, when a
registered user is trying to log in but forgot their password, they can ask for a reset password which will send an
email with a unique link to reset it.

### Dash Integration:

The dashboard developed during cw-1 has been integrated using the navigation bar. This has allowed the integration of
multiple pages of the originally developed dash app, resulting in a multi-page dashboard available to the user. 