from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length
from flask_babel import _, lazy_gettext as _l
from app.models import User, Subscribe
from flask_ckeditor import CKEditorField

from wtforms.ext.sqlalchemy.fields import QuerySelectField


class EditProfileForm(FlaskForm):
    """
    Form for editing users profile
    """
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'),
                             validators=[Length(min=0, max=140)])
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))


class PostForm(FlaskForm):
    """
    Form for creating new post
    """
    post = CKEditorField(_l('Say something'))
    submit = SubmitField(_l('Submit'))


class CommentForm(FlaskForm):
    """
    Form for creating new comment
    """
    post = TextAreaField(_l('Comment post'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class SubscribeForm(FlaskForm):

    def get_subscribes():
        return Subscribe.query.order_by(Subscribe.id).all()

    subs = QuerySelectField('Subscribe', query_factory=get_subscribes, validators=[DataRequired()])
    life_time = SelectField(_l('Duration'), choices=[('1', '1 month'),
                                                     ('3', '3 months '),
                                                     ('6', '6 months'),
                                                     ('12', '1 Year'),
                                                     ('24', '2 Years')
                                                     ])
    submit = SubmitField(_l('Submit'))
