from flask_bcrypt import bcrypt
from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from facial.models import User
from facial import bcrypt

class RegistrationForm(FlaskForm):
    username = StringField('UserName:',validators=[DataRequired(),Length(min=2,max=15)])
    
    email = StringField("Email:",validators=[DataRequired(),Email()])
    
    password = PasswordField('Password:',validators=[DataRequired(),Length(min=6)])
    
    confirm_password = PasswordField('Confirm Password:',validators=[DataRequired(),Length(min=6),EqualTo('password')])
    
    submit = SubmitField('Sign up')
    
    def validate_username(self,username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is taken. Please try another username')
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists.')

class LoginForm(FlaskForm):
    email = StringField("Your Email:",validators=[DataRequired(),Email()])
    
    password = PasswordField('Your Password:',validators=[DataRequired(),Length(min=6)])
    
    submit = SubmitField('Log in')

class UpdateAccountForm(FlaskForm):
    username = StringField('UserName:',validators=[DataRequired(),Length(min=2,max=15)])
    
    email = StringField("Email:",validators=[DataRequired(),Email()])

    current_password = PasswordField('Current Password:',validators=[DataRequired(),Length(min=6)])

    password = PasswordField('New Password:',validators=[Length(min=6)])

    confirm_password = PasswordField('Confirm Password:',validators=[Length(min=6),EqualTo('password')])

    submit = SubmitField('Update')
    
    def validate_username(self,username):
        if current_user.username != username.data:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is taken. Please try another username')
        
    def validate_email(self,email):
        if current_user.email != email.data:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists.')
            
    # check if user inputs the right current password before updating their password
    def validate_current_password(self,current_password):
        if not bcrypt.check_password_hash(current_user.password,current_password.data):
            raise ValidationError("Please enter the correct current password")

class RequestResetForm(FlaskForm):
    email = StringField("Your Email:",validators=[DataRequired(),Email()])
    submit = SubmitField('Request Password Reset')
    
    #Ensure user does not sumbit an invalid email when requesting a password reset
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('Account does not exist. Please create an account first')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password:',validators=[DataRequired(),Length(min=6)])
    
    confirm_password = PasswordField('Confirm Password:',validators=[DataRequired(),Length(min=6),EqualTo('password')])
    
    submit = SubmitField('Reset Password')
