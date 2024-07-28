from datetime import datetime
from Flaskblog import db, loginmanager
from flask import current_app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

@loginmanager.user_loader
def load_user(user_Id: int):
    return User.query.get(int(user_Id))

class User(db.Model, UserMixin):
    """Hnadling DataBase User Part"""
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(19), nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(25), nullable=False, default='default.jpg')
    Password = db.Column(db.String(60), nullable=False)
    Posts = db.relationship('Post', backref='author', lazy=True)
    
    def get_reset(self, expires_sec=60):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
        
    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = Serializer(current_app.config['SECRET_KEY'])\
            .loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


    def __repr__(self):
        return f"User('{self.Username}, {self.Email}, {self.image_file},')"
class Post(db.Model):
    """Hnadling DataBase Post Part"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    post_Date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"Post('{self.title}, {self.post_Date}')"
