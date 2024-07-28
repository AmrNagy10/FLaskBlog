from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
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
    
class UpdateForm(FlaskForm):
    username =  StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=15)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    Submit = SubmitField('Update !')

    def validate_email(self, email):
        if email.data != current_user.Email:
            if User.query.filter_by(Email=email.data).first():
                raise ValidationError('This Email Is already Taken !. Please Try With another Email')

class requestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    Submit = SubmitField('Request Password Reset !')

    def validate_email(self, email):
        if User.query.filter_by(Email=email.data).first() is None:
            raise ValidationError('There is no Email you must Register first .')
    
    
class ResePassword(FlaskForm):
    password = PasswordField('Password',
                              validators=[DataRequired(), Length(min=6,max=12)])
    confirm_password = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    Submit = SubmitField('Reset Password')

