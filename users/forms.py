import re
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import Required, Email, Length, EqualTo, ValidationError


def character_check(form,field):
    excluded_chars = "*?"
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f"Character {char} is not allowed.")


class RegisterForm(FlaskForm):
    username = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required(),
                                         Length(min=8, max=15, message='Password must be between 8 and 15 characters in length.'),
                                         character_check])
    confirm_password = PasswordField(validators=[Required(), EqualTo('password', message='Both password fields must be equal!')])
    pinkey = StringField(validators=[Required(), character_check, Length(max=32, min=32, message="Length of PIN key must be 32.")])
    submit = SubmitField()

    def validate_password(self, password):
        p = re.compile(r'(?=.*\d)(?=.*[A-Z])')
        if not p.match(self.password.data):
            raise ValidationError("Password must contain at least 1 digit and 1 uppercase letter.")


class LoginForm(FlaskForm):
    username = StringField(validators=[Required(), Email()])
    password = PasswordField(validators=[Required()])
    pin = StringField(validators=[Required()])
    recaptcha = RecaptchaField()
    submit = SubmitField()

    def validate_pin(self, pin):
        pi = re.compile(r'^(?:\s*)\d{6}(?:\s*)$')
        if not pi.match(self.pin.data):
            raise ValidationError("PIN must only contain integers and have a length of 6.")
