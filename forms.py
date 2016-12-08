from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Email, Length


class SignupForm(FlaskForm):
    firstname = StringField(
        'First name', validators=[DataRequired("Please enter your first name.")])
    lastname = StringField('Last name', validators=[DataRequired("Please enter your last name.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address."),
                                             Email("Please enter your email address.")])
    password = PasswordField('Password', validators=[DataRequired("Please enter a password."),
                                                     Length(min=8, message="Passwords must be 8 characters or more.")])
    submit = SubmitField('Sign up')


class LoginForm(FlaskForm):
    email = StringField(
        'Email', 
        validators=[
            DataRequired("Please enter your email address."),
            Email("Please enter your email address.")
        ]
    )
    password = PasswordField(
        'Password', 
        validators=[
            InputRequired(), 
            EqualTo('confirm', message='Passwords must match')
        ]
    )
    submit = SubmitField("Sign in")

