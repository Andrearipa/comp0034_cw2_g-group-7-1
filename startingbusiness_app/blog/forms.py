from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length

from startingbusiness_app.models import Blog


class CreateNewPost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=50)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=2, max=500)])
    submit_post = SubmitField('Create Post')


class ModifyPost(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=50)])
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=2, max=500)])
    submit_post = SubmitField('Update Post')

class Post(FlaskForm):
    pass

class DeletePost(FlaskForm):
    pass