from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from Flaskblog import db, bcrypt
from Flaskblog.Modules import User, Post
from Flaskblog.users.forms import RegistrationForm, LoginForm, UpdateForm, requestResetForm, ResePassword
from Flaskblog.users.utils import save_picture, send_reset_email

users =Blueprint('users', __name__)

@users.route("/register", methods=['GET','POST'])
def register():
    """Register Page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(Username=form.username.data, Email=form.email.data, Password=hashed_pw) # type: ignore
        db.session.add(user)
        db.session.commit()
        flash('Your Account has been created !', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET','POST'])
def login():
    """Login Page"""
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.Password, form.password.data):
            login_user(user=user,remember=form.remember.data)
            flash('Your password has been updated! You have been logged in .', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('users.login'))

        else:
            flash('Login Unsuccessful ! Please try check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
    """logout def """
    logout_user()
    return redirect(url_for('users.account'))



@users.route("/account", methods=['GET','POST'])
@login_required
def account():
    """Account Def"""
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            if picture_file:
                current_user.image_file = picture_file
        current_user.Username = form.username.data
        current_user.Email = form.email.data
        db.session.commit()
        flash('Your profile has been updated !', 'success')
        return redirect(url_for('users.account'))
    elif request.method =='GET':
        form.username.data = current_user.Username
        form.email.data = current_user.Email

    image_file = url_for('static', filename='ProfilePic/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@users.route("/user/<string:username>")
@login_required
def user_post(username):
    """Home Page"""
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(Username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
    .order_by(Post.post_Date.desc())\
    .paginate(page=page,per_page=10)
    return render_template('Userpost.html', posts=posts, user=user)

@users.route("/reset_password", methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = requestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(Email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form= form)

@users.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is Invalid token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResePassword()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.Password = hashed_pw
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form= form)

