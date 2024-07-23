from datetime import datetime
from Flaskblog import db

class User(db.Model):
    """Hnadling DataBase User Part"""
    id = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(19), unique=True, nullable=False)
    Email = db.Column(db.String(120), unique=True, nullable=False)
    Image_Files = db.Column(db.String(25), nullable=False, default='default.jpg')
    Password = db.Column(db.String(60), nullable=False)
    Posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.Username}, {self.Email}, {self.Image_Files},')"
    
class Post(db.Model):
    """Hnadling DataBase Post Part"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    post_Date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}, {self.post_Date}')"

