from ast import Pass
from operator import le, length_hint
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField, SearchField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from dict.models import User

class SearchForm(FlaskForm):
    searched = StringField(label='Searched', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')
    

    