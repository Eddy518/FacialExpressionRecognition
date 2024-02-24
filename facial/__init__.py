from flask import Flask
app = Flask(__name__)
app.config['SECRET_KEY'] ='927af1257ba908bea162f42b2011047f'

from facial import routes

