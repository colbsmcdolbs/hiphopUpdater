from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms import validators
from wtforms.fields.html5 import EmailField


class UnsubForm(FlaskForm):
    email = EmailField('Email Address', [validators.DataRequired(), 
            validators.Email()])
    submit = SubmitField('Unsubscribe')
