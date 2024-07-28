"""Importing Modules Flaskblog """
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from Flaskblog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
loginmanager = LoginManager()
loginmanager.login_view = 'users.login'
loginmanager.login_message_category = 'info'
mail = Mail()



def create_app(config_class=Config):
    app = Flask(__name__, template_folder='Templates')
    app.config.from_object(Config)
    db.init_app(app)
    bcrypt.init_app(app)
    loginmanager.init_app(app)
    mail.init_app(app)
    from Flaskblog.users.routes import users
    from Flaskblog.posts.routes import posts
    from Flaskblog.main.routes import main
    from Flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app