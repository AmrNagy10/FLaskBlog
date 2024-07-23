from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired ,Length, Email, EqualTo
from Flaskblog.Modules import User
class RegistrationForm(FlaskForm):
    username =  StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6,max=12)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    Submit = SubmitField('Sign Up')

    def validate_email(self, email):
        if User.query.filter_by(Email=email.data).first():
            raise ValidationError('This Email Is already Taken !. Please Try With another Email')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6,max=12)])
    remember = BooleanField('Remember Me')
    Submit = SubmitField('Login')
