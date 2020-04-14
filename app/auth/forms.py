from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_babel import _, lazy_gettext as _l
from app.models import User, Country
from wtforms.fields.html5 import DateField
from datetime import date


class LoginForm(FlaskForm):
    """
    Form for users Login
    """
    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    """
    Form for users Registration
    """

    def get_countries():
        return Country.query.order_by(Country.id).all()

    username = StringField(_l('Username'), validators=[DataRequired()])
    first_name = StringField(_l('First Name'))
    last_name = StringField(_l('Last Name'))
    birthday = DateField(_l('Birthday'), format='%Y-%m-%d')
    country = QuerySelectField('Country', query_factory=get_countries, validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        """
        Validates username, checks if it is unique

        :param username: provided username
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        """
        Validates email, checks if it is unique

        :param email: provided email
        """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))

    def validate_birthday(self, birthday):
        if birthday.data >= date.today():
            raise ValidationError(_('Please use a different date.'))


class ResetPasswordRequestForm(FlaskForm):
    """
    Form sending request for reset password
    """
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    """
    Form for reset password
    """
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(
        _l('Repeat Password'), validators=[DataRequired(),
                                           EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))
