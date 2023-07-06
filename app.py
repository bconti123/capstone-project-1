import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

from models import db, connect_db, User, Card, View

CURR_USER_KEY = 'curr_user'
CURR_LOGIN_KEY = 'curr_login_user'

app = Flask(__name__)
app.app_context().push() # Flask latest version does need this.

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///yugioh_eff_checker'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['FLASK_DEBUG'] = True
toolbar = DebugToolbarExtension(app)

connect_db(app)

db.create_all()