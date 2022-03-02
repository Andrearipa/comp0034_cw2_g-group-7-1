from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from startingbusiness_app.models import User


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
    profile_image = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'],
                                                                                message="png and jpg formats only supprted")])
    submit = SubmitField('Update')

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError('An account is already registered for that email address')
