from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class RegisterForm(FlaskForm):
    username = StringField()
    submit = SubmitField()

