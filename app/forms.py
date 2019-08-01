from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from wtforms import validators
from wtforms.fields.html5 import EmailField


class UnsubForm(FlaskForm):
    email = EmailField('Email Address', [validators.DataRequired(), 
            validators.Email()])
    submit = SubmitField('Unsubscribe')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email does not exist in our database.')