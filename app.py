import os

from flask import Flask, render_template, session, g
from flask_debugtoolbar import DebugToolbarExtension
from forms import SearchForm
from models import db, connect_db, User, View

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

@app.before_request
def before_request_global():
    """If visit any website routes, add guest user session to Flask global """
    if not CURR_USER_KEY in session:
        guest = User.guest_visit()
        session[CURR_USER_KEY] = guest.id

    if CURR_LOGIN_KEY in session:
        del session[CURR_USER_KEY]
    
@app.before_request
def add_user_to_g():
    """ When we logged in, the website detect global login users """
    if CURR_LOGIN_KEY in session:
        g.user = User.session.get(session[CURR_LOGIN_KEY])
    else:
        g.user = None
    
    def do_login(user):
        session[CURR_LOGIN_KEY] = user.id
    
    def do_logout(user):

        if CURR_LOGIN_KEY in session:
            del session[CURR_LOGIN_KEY]


@app.route('/')
def homepage():
    form = SearchForm()
    return render_template('/index.html', form=form)


### User Routes ###
@app.route('/users/register')
def register():
    user_id = session[CURR_USER_KEY]
    return render_template('/users/register.html')