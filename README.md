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
if we have been following a general guideline, insert the reference here
if we have copied code specifically, we can reference it within the py file itself -> to be done for the blog