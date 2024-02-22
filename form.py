from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('UserName:',validators=[DataRequired(),Length(min=2,max=15)])
    
    email = StringField("Email:",validators=[DataRequired(),Email()])
    
    password = PasswordField('Password:',validators=[DataRequired(),Length(min=6)])
    
    confirm_password = PasswordField('Confirm Password:',validators=[DataRequired(),Length(min=6),EqualTo('password')])
    
    submit = SubmitField('Sign up')
    
class LoginForm(FlaskForm):
    email = StringField("Your Email:",validators=[DataRequired(),Email()])
    
    password = PasswordField('Your Password:',validators=[DataRequired(),Length(min=6)])
    
    submit = SubmitField('Log in')