from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, DateField, SelectField
from wtforms.validators import Required

class PostForm(FlaskForm):
    post_title = StringField('title',validators=[Required()])
    post = TextAreaField('Content')
    submit = SubmitField('Submit')

class CommentsForm(FlaskForm):
    author = StringField('Name',validators = [Required()])
    comment = TextAreaField('Comment here')
    submit = SubmitField('Submit')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('about you.',validators = [Required()])
    submit = SubmitField('Submit')

class UpdatePost(FlaskForm):
    post_title = StringField('title',validators=[Required()])
    post = TextAreaField('Edit post',validators = [Required()])
    submit = SubmitField('Submit')

class EmailForm(FlaskForm):
    name = StringField('Name',validators=[Required()])
    email = StringField('Email Address',validators=[Required()])
    subscribe = SubmitField('Subscribe to get notifications from us')