from flask import Blueprint, render_template,request
from flask_login import login_required
from Flaskblog.Modules import Post

main =Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
@login_required
def home():
    """Home Page"""
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.post_Date.desc()).paginate(page=page,per_page=10)
    return render_template('Home.html', posts=posts)

@main.route("/about")
def about():
    """About Page"""
    return render_template('About.html', title='About')