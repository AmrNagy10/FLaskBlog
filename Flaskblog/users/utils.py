import os, secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from Flaskblog import db, bcrypt, mail
from Flaskblog.Modules import User, Post
from flask import url_for, current_app
from flask_mail import Message
from flask_login import login_user, current_user, logout_user, login_required



def save_picture(formPicture):
    """Handel Image While Uploading And Set Size And if user change his image it remove old one"""
    random_hex = secrets.token_hex(8)
    old_picture_filename = current_user.image_file
    picture_fn = random_hex + '.png'
    picture_path = os.path.join(current_app.root_path, 'static/ProfilePic', picture_fn)
    Output_Size = (400,400)
    point = Image.open(formPicture)
    point.thumbnail(Output_Size)
    point.save(picture_path, format='PNG')
    if old_picture_filename:
        old_picture_path = os.path.join(current_app.root_path, 'static/ProfilePic', old_picture_filename)
        if os.path.exists(old_picture_path) and 'default' not in old_picture_filename:
            os.remove(old_picture_path)
    return picture_fn


def send_reset_email(User):
    token = User.get_reset()
    msg = Message('Password Reset request', sender='noreply@demo.com', recipients=[User.Email])
    msg.body= f'''To reset your password, Visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request, ignore this email and no changes will be made.
    '''
    mail.send(msg)