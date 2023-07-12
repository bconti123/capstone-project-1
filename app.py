import os

from flask import Flask, render_template, session, g, flash, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from forms import SearchForm, UserAddForm, LoginForm
from models import db, connect_db, User, View
from sqlalchemy.exc import IntegrityError

import requests

CURR_USER_KEY = 'curr_user'
CURR_LOGIN_KEY = 'curr_login_user'
BASE_API_KEY = 'https://db.ygoprodeck.com/api/v7/cardinfo.php'

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
    # When logged user id and guest user id are same, delete guest user id in session.

@app.before_request
def add_g_user():
    """ When we logged in, the website detect global login users """
    if CURR_LOGIN_KEY in session:
        g.user = db.session.get(User, session[CURR_LOGIN_KEY])
        if g.user.id == session.get(CURR_USER_KEY):
            del session[CURR_USER_KEY]
    else:
        g.user = None

# Login and Logout functions    
def do_login(user):
    session[CURR_LOGIN_KEY] = user.id

def do_logout():
    if CURR_LOGIN_KEY in session:
        del session[CURR_LOGIN_KEY]



@app.route('/')
def homepage():
    return render_template('/index.html')

### User Routes ###
@app.route('/users/register', methods=['GET', 'POST'])
def register():
    user_id = session[CURR_USER_KEY]
    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                user_id,
                form.username.data,
                form.password.data,
                form.email.data,
            )
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('/users/register.html', form=form)
        
        do_login(user)

        return redirect('/')
    else:
        return render_template('/users/register.html', form=form)

@app.route('/users/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f'Hello, {user.username}!', 'success')
            return redirect('/')
        
        flash('Invalid credentials.', 'danger')
    
    return render_template('/users/login.html', form=form)

@app.route('/logout')
def logout():
    do_logout()
    flash('Logout successfully', 'success')
    return redirect('/')


# Card functions
def search_card(card):
    try: 
        response = requests.get(f'{BASE_API_KEY}?fname={card}')
        response.raise_for_status()
        obj = response.json()
        if 'data' in obj:
            return obj['data']
        else:
            return []
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f'Error: {e}')
        return []

def find_card_id(id):
    try: 
        response = requests.get(f'{BASE_API_KEY}?id={id}')
        response.raise_for_status()
        obj = response.json()
        if 'data' in obj:
            return obj['data']
        else:
            return []
    except (requests.exceptions.RequestException, ValueError) as e:
        print(f'Error: {e}')
        return []

def find_card_desc(card):
    desc_list = card[0]['desc'].split('. ')
    result_list = []
    cond_obj = {}
    cost_obj = {}
    act_obj = {}
    for desc in desc_list:

        if ":" in desc:
            cond = desc.index(":")

            substring = desc[0:cond+1]
            
            cond_obj = {'condition' : substring}
            desc = desc.replace(substring, '')
        if ";" in desc:
            cost = desc.index(";")
            substring = desc[0:cost+1]
        
            cost_obj = {'cost' : substring}
            desc = desc.replace(substring, '')
        
        act_obj = {'act': desc}
        # ISSUES: dot '●', Fix it later.
        result_list.append({**cond_obj, **cost_obj, **act_obj})

    return result_list

# Card API Route
@app.route('/cards')
def card_search():
    cards = search_card(request.args.get('search'))
    return render_template('/index.html', data=cards)

@app.route('/cards/<int:card_id>')
def card_show(card_id):
    card = find_card_id(card_id)
    desc_list = find_card_desc(card)

    return render_template('/cards/detail.html', data=card, desc_list=desc_list)