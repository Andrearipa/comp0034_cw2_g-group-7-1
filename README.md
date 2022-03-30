# COMP0034 - Group 7 - Coursework 2

## Introduction
[Repository-Link](https://github.com/ucl-comp0035/comp0034_cw2_g-group-7-1)
[Explanatory Video Link](https://youtu.be/55oP3qd0A2k)

The team decided to develop a web app to integrate the dashboard with more functionalities. The functionalities
developed are based on the requirements highlighted in the first part of the project (Term 1). The functionalities taken
in consideration were also classified based on the importance. This ranking was used to prioritize the features to be
developed considering the time and resource constraint. Based on the aforementioned information, the features that the
team chose to develop are:

- Sign-up
- Log in/out
- Profile (inc. picture)
- Blog
- Email Integration
- Dash Integration

All the features were developed using a blueprint structure and specific templates (html) and static files for style
(css).

### Sign-Up:

The sign-up was developed to allow the user to register to access some additional functionalities. It is important to
mention that since the beginning of the project the team has always agreed that the dashboard should have been
accessible to any user. For this reason the additional features were then developed accordingly, based on whether the
user is a guest (not-registered) or has a profile. In this way the purpose of creating a platform to share information
about starting a business would be met.

The sign-up consists in a quick form to fill with info about first name, surname, email, password and type of use. In
addition, there is also the possibility of adding a profile picture, if none is chosen than a default one is assigned.
Hashing of images was also performed to avoid possible name duplicates. The password is hashed before storing it for
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

## Testing

Please note that the testing run through the terminal will not work on Windows machine for the browser test only. This
is due to the 'fork' argument for multiprocessing not working on Windows. 'Spawn' can be used instead as an argument,
but it will not run on GitHub.

## References

Some functionalities of the web app were based on the tutorial videos of Corey Schafer for 'flask tutorial'
[link](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH). The functionalities that are presented
in the tutorial were used as inspiration, but they were rewritten to match the web application purpose and needs. The
GitHub code of the tutorial can be found at the following 
[link](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog). The main feature that was based on 
the tutorial was the overall structure of the blog even though it was adapted, modified to have more functionalities and 
also the style and templates were changed. 
