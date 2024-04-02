from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    SelectField,
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    Optional,
    ValidationError,
)
from . import Provider, Customer


class SignUpForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
