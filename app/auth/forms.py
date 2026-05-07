from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email    = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit   = SubmitField('Log in')


class RegisterForm(FlaskForm):
    username  = StringField('Username',
                            validators=[DataRequired(), Length(min=3, max=64)])
    email     = StringField('Email', validators=[DataRequired(), Email()])
    password  = PasswordField('Password',
                              validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField('Repeat password',
                              validators=[DataRequired(), EqualTo('password')])
    submit    = SubmitField('Create account')
