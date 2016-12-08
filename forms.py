from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField
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

# TO-DO: input constraint
class saveOrderForm(FlaskForm):
    type = StringField(
        'Type',
        validators=[
            DataRequired("Please enter order type.")
        ]
    )

    size = IntegerField(
        'Size',
        validators=[
            DataRequired("Please enter order size.")
        ]
    )

    inventory = IntegerField(
        'Inventory',
        validators=[
            DataRequired("Please enter order inventory.")
        ]
    )

class saveTradeForm(FlaskForm):
    type = StringField(
        'Type',
        validators=[
            DataRequired("Please enter trade type.")
        ]
    )

    price = FloatField(
        'Price',
        validators=[
            DataRequired("Please enter trade price.")
        ]
    )

    shares = FloatField(
        'Shares',
        validators=[
            DataRequired("Please enter trade shares.")
        ]
    )

    notional = FloatField(
        'Notional',
        validators=[
            DataRequired("Please enter trade notional.")
        ]
    )

    status = StringField(
        'Status',
        validators=[
            DataRequired("Please enter trade status.")
        ]
    )