"""
This file is used for the definitions of forms used in the authentication blueprint. It comprises the forms for the sign
up, log in, update profile and reset password. It also adds different validation functions for the forms.
"""

from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField, PasswordField, EmailField, BooleanField, SelectField, SubmitField, FileField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from startingbusiness_app import photos
from startingbusiness_app.models import User


class SignupForm(FlaskForm):
    first_name = StringField(label='First name', validators=[DataRequired(message='First name is required'),
                                                             Length(min=2, max=20)])
    last_name = StringField(label='Last name', validators=[DataRequired(message='Last name is required'),
                                                           Length(min=2, max=16)])
    email = EmailField(label='Email address', validators=[DataRequired(message='Email address is required'),
                                                          Length(min=5,
                                                                 message="Email address is not valid (too short)")])
    password = PasswordField(label='Password', validators=[DataRequired(message='Password is required'),
                                                           Length(min=5,
                                                                  message="Password must be at least 10 characters")])
    password_repeat = PasswordField(label='Confirm Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    account_type = SelectField(label='Intended Use', choices=[('Professional', 'Professional'), ('Student', 'Student'),
                                                              ('Entrepreneur', 'Entrepreneur')],
                               validators=[DataRequired(message='This field is required')])
    photo = FileField(label='Profile Picture', validators=[FileAllowed(photos, message='png and jpg formats only')])
    submit_reg = SubmitField('Register')

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered with this email address')


class LoginForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')
    submit_login = SubmitField('Login')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account found with that email address.')

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError('No account found with that email address.')
        if not user.check_password(password.data):
            raise ValidationError('Incorrect password.')


class UpdateProfileForm(FlaskForm):
    first_name = StringField(label='First name', validators=[DataRequired(message='First name is required'),
                                                             Length(min=2, max=20)])
    last_name = StringField(label='Last name', validators=[DataRequired(message='Last name is required'),
                                                           Length(min=2, max=12)])
    email = EmailField(label='Email address', validators=[DataRequired(message='Email address is required'),
                                                          Length(min=5,
                                                                 message="Email address is not valid (too short)")])
    account_type = SelectField(label='Intended Use', choices=[('Professional', 'Professional'), ('Student', 'Student'),
                                                              ('Entrepreneur', 'Entrepreneur')],
                               validators=[DataRequired(message='This field is required')])
    photo = FileField(label='Profile Picture', validators=[FileAllowed(photos, message='png and jpg formats only')])
    submit_reg = SubmitField('Update Profile Info')

    def validate_email(self, email):
        if email.data != current_user.email:
            users = User.query.filter_by(email=email.data).first()
            if users is not None:
                raise ValidationError('An account is already registered with this email address')


class ResetPasswordRequestForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    submit_reset = SubmitField('Send Reset Email')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('No account found linked to that email address.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(label='Password', validators=[DataRequired(message='Password is required'),
                                                           Length(min=5,
                                                                  message="Password must be at least 5 characters")])
    password_repeat = PasswordField(label='Confirm Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit_new_pw = SubmitField('Reset Password')
