"""
This file is used for the definitions of forms used in the blog blueprint. It comprises the forms for the blog page,
create a new post and modify/delete it.
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, RadioField
from wtforms.validators import DataRequired, Length


class BlogPage(FlaskForm):
    # add_post_button = SubmitField('Write a new post')
    filter_keyword = StringField('Keyword search')
    sort_by = RadioField('Sort posts by:', choices=[('date_new', 'Date - Newest'),
                                                    ('date_old', 'Date - Oldest'),
                                                    ('title', 'Title')], default='date_new')


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
