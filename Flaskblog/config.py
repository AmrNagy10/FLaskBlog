import os

class Config:
    basedir = os.path.abspath(os.path.dirname(__file__))
    database_path = os.path.join(basedir, 'Database', 'site.db')
    os.makedirs(os.path.dirname(database_path), exist_ok=True)
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{database_path}'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')