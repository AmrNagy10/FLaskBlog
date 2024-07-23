"""Importing Modules Flaskblog """
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt


basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'Database', 'site.db')
os.makedirs(os.path.dirname(database_path), exist_ok=True)
app = Flask(__name__, template_folder='Templates')
app.config['SECRET_KEY'] = 'e7bbc4321343f720c5c1ec79e805c1cd'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app=app)

from Flaskblog import routes