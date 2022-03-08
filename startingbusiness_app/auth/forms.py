from flask_wtf.file import FileAllowed
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, EmailField, BooleanField, SelectField, FileField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from startingbusiness_app import photos
from startingbusiness_app.models import User


class SignupForm(FlaskForm):

    first_name = StringField(label='First name', validators=[DataRequired(message='First name required'),
                                                             Length(min = 4, max = 12 )])
    last_name = StringField(label='Last name', validators=[DataRequired(message='Last name required'),
                                                           Length(min = 4, max = 12 )])
    email = EmailField(label='Email address', validators=[DataRequired(message='Email address required'),
                                                          Length(min = 5, message= "Email address too short")])
    password = PasswordField(label='Password', validators=[DataRequired(message='Password required'),
                                                           Length(min=10, message="Password must be at least 10 characters long")])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    account_type = SelectField(label='Intended Use', choices=[('Professional', 'Professional'), ('Student', 'Student'),
                                                             ('Entrepreneur', 'Entrepreneur')],
                                  validators=[DataRequired(message='This field is required')])
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])


    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')


class LoginForm(FlaskForm):
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')

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



class UpdateAccountForm(FlaskForm):
    first_name = StringField(label='First name', validators=[DataRequired(message='First name required'),
                                                             Length(min=4, max=12)])
    last_name = StringField(label='Last name', validators=[DataRequired(message='Last name required'),
                                                           Length(min=4, max=12)])
    email = EmailField(label='Email address', validators=[DataRequired(message='Email address required'),
                                                          Length(min=5, message="Email address too short")])
    account_type = SelectField(label='Intended Use', choices=[('Professional', 'Professional'), ('Student', 'Student'),
                                                              ('Entrepreneur', 'Entrepreneur')],
                               validators=[DataRequired(message='This field is required')])
    #profile_image = FileField(label='image',
                              #validators=[FileAllowed(['jpg', 'png'], message='png and jpg formats only')])
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])
    submit = SubmitField('Update')

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')
