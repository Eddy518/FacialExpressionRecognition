from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] ='927af1257ba908bea162f42b2011047f'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] =  True
app.config['MAIL_USERNAME'] = 'edmwangi2@gmail.com'
app.config['MAIL_PASSWORD'] = 'fswo vtms qxyt kikc'

mail = Mail(app)

from facial import routes

