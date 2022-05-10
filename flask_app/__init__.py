# 3rd-party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_login import (
    LoginManager,
    current_user,
    login_user,
    logout_user,
    login_required,
)
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename

#from flask_mail import Mail #note: do not need to import flask_mail, just need to import Mail from flask_mail

# stdlib
from datetime import datetime
import os

# local


db = MongoEngine()
login_manager = LoginManager()

bcrypt = Bcrypt()

'''
app = Flask(__name__)
app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	#MAIL_SERVER='smtp.gmail.com',
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
	MAIL_SENDER = 'fooddiaries1212@outlook.com',
	MAIL_PASSWORD = 'fooddiariespassword2'
	)
mail = Mail(app)
'''

from .routes import main

#from .extensions import mail #added

def page_not_found(e):
    return render_template("404.html"), 404


def create_app(test_config=None):
    app = Flask(__name__) #moved up! (to be able to access in other folders)
    app.config.from_pyfile("config.py", silent=False)
    #app.config["MONGODB_HOST"] = os.getenv("MONGODB_HOST")

    app.config["MONGOB_HOST"] = "mongodb+srv://admin_user:ZOS242hRMvGjXLse@cluster0.m04uq.mongodb.net/final_project?retryWrites=true&w=majority" #!!!comment out if need to
    
    if test_config is not None:
        app.config.update(test_config)

    '''
    #Just added the three configs below for using flask-mail
    app.config['MAIL_PASSWORD'] = "fooddiariespassword2" #os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_SENDER'] = "fooddiaries1212@outlook.com" #os.environ.get('MAIL_SENDER')
    app.config['MAIL_PORT'] = 465 #os.environ.get('MAIL_PORT') - this mail work isn't working, see what happens when i comment it out!
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True

    #mail = Mail(app) #moved up 
    mail.init_app(app) #Just added -make sure this doesn't break anything (bc not sure if can have two init_app called!)
    '''
    '''
    from .extensions import mail, login_manager, db #new - remove if mail doesn't work
    #####
    #New - remove if mail is not working! (this update sections)
    #if doesn't work - try to change the mail server after enabling 2 factor authentication on gmail!
    mail.init_app(app)#new - remove if mail doesn't work

    app.config.update(dict(
        DEBUG=True,
        #EMAIL SETTINGS
        MAIL_SERVER='smtp.gmail.com',
        MAIL_PORT = 587,
        MAIL_USE_TLS = True,
        MAIL_USE_SSL = False,
        MAIL_SENDER = 'mkmoonlight14@gmail.com',
        MAIL_PASSWORD = 'MoonlightSonata2'
    ))
    #######
    '''

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    app.register_blueprint(main)
    app.register_error_handler(404, page_not_found)


    login_manager.login_view = "main.login"

    return app