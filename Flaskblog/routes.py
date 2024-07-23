"""Importing Modules """
from flask import render_template, url_for, flash, redirect
from Flaskblog import app, db, bcrypt
from Flaskblog.forms import RegistrationForm, LoginForm
from Flaskblog.Modules import User, Post
from flask_login import login_user, current_user, logout_user



posts = [
    {
        'Auther':'Amr Nagy',
        'Post':'I`m a Python Developer',
        'Date_posted':'jue 20 , 2006',
        'Title':'Hello It`s me'
    },

    {
        'Auther':'Yassen Nagy',
        'Post':'I`m a Web Developer',
        'Date_posted':'jue 25 , 2010',
        'Title':'Hello It`s Yassen'
    }
]


@app.route("/")
@app.route("/home")
def home():
    """Home Page"""
    return render_template('Home.html', posts=posts)

@app.route("/about")
def about():
    """About Page"""
    return render_template('About.html', title='About')

@app.route("/register", methods=['GET','POST'])
def register():
    """Register Page"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(Username=form.username.data, Email=form.email.data, Password=hashed_pw) # type: ignore
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created !', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    """Login Page"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.Password, form.password.data):
            login_user(user=user,remember=form.remember.data)
            flash('You have been logged in .', 'success')
            return redirect(url_for('home'))

        else:
            flash('Login Unsuccessful ! Please try check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    """logout def """
    logout_user()
    return redirect(url_for('home'))

