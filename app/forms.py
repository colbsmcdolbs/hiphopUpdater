from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators, SelectMultipleField
from wtforms.validators import DataRequired
from wtforms.fields.html5 import EmailField
from flask_select2.model.fields import AjaxSelectField, AjaxSelectMultipleField
from flask_select2.contrib.sqla.ajax import QueryAjaxModelLoader
from app import db, select2
from app.models import Rapper


class UnsubForm(FlaskForm):

    email = EmailField('Email Address', [validators.DataRequired(), 
            validators.Email()])
    submit = SubmitField('Unsubscribe')


class SignUpForm(FlaskForm):

    rapper_loader = QueryAjaxModelLoader(
        name='rapper',
        session=db.session,
        model=Rapper,
        fields=['name'],
        order_by=[Rapper.name.asc()],
        page_size=5,
        placeholder="Select your favorite rappers...")

    select2.add_loader(loader=rapper_loader)

    email = EmailField('Email Address', [validators.DataRequired(), 
            validators.Email()])

    rappers = AjaxSelectMultipleField(
        loader=rapper_loader,
        label='Rappers',
        allow_blank=False
    )

    submit = SubmitField('Sign Me Up!')
