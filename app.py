import os
from flask import Flask, render_template, session, g, flash, redirect, request, url_for
from forms import UserAddForm, LoginForm
from models import db, connect_db, User, View, Comment
from sqlalchemy.exc import IntegrityError
from ygo import find_card_desc, find_card_id, search_card
from math import ceil

CURR_USER_KEY = 'curr_user'
CURR_LOGIN_KEY = 'curr_login_user'

app = Flask(__name__)
app.app_context().push() # Flask latest version does need this.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)

db.create_all()

@app.before_request
def add_g_user():
    """ When we logged in, the website detect global login users """
    if CURR_LOGIN_KEY in session:
        g.user = db.session.get(User, session[CURR_LOGIN_KEY])
        if g.user.id == session.get(CURR_USER_KEY):
            del session[CURR_USER_KEY]
    else:
        g.user = None

    if CURR_USER_KEY in session:
        g.guest = db.session.get(User, session[CURR_USER_KEY])
    else:
        g.guest = None

# Login and Logout functions    
def do_login(user):
    session[CURR_LOGIN_KEY] = user.id

def do_logout():
    if CURR_LOGIN_KEY in session:
        del session[CURR_LOGIN_KEY]

    if not CURR_USER_KEY in session:
        guest = User.guest_visit()
        session[CURR_USER_KEY] = guest.id

def do_guest():
    guest = User.guest_visit()
    session[CURR_USER_KEY] = guest.id
    return guest.id

# Homepage Route #
@app.route('/')
def homepage():
    return render_template('/index.html')

### User Routes ###
@app.route('/users/register', methods=['GET', 'POST'])
def register():
    """ For user, register account """
    if g.user:
        flash("You're already logged in.", "danger")
        return redirect('/')
    
    if g.guest:
        user_id = g.guest.id
    else:
        user_id = do_guest()

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
    """ User log in """
    if g.user:
        flash("You're already logged in.", "danger")
        return redirect('/')
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
    """ User log out"""
    if not g.user:
        flash('Access unauthorized.', 'danger')
    do_logout()
    flash('Logout successfully', 'success')
    return redirect('/')

# Card API Route
@app.route('/cards')
def card_search():
    """ Search cards from YGO API and Pagination """
    page = request.args.get('page', 1, type=int)
    search_term = request.args.get('search')
    cards = search_card(search_term)

    per_page = 10
    total_pages = ceil(len(cards) / per_page)
    offset = (page - 1) * per_page

    paginated_cards = cards[offset:offset + per_page]

    return render_template('/listing.html',
                            data=paginated_cards, 
                            data_cards=cards, 
                            search_term=search_term, 
                            page=page, 
                            per_page=per_page, 
                            total_pages=total_pages)

@app.route('/cards/<int:card_id>')
def card_show(card_id):
    """ Show Card Detail """
    if not g.guest and not g.user:
        guest = User.guest_visit()
        session[CURR_USER_KEY] = guest.id

    card = find_card_id(card_id)
    desc_list = find_card_desc(card)
    if g.user:
        user_id = g.user.id
    else:
        user_id = session[CURR_USER_KEY]
    View.seen_card(user_id, card_id)

    views = db.session.query(View).filter_by(card_api_id=card_id).all()

    com_list = db.session.query(Comment).filter_by(card_api_id=card_id).all()

    for comment in com_list:
        comment.created_at = comment.created_at.strftime('%B %d, %Y - %I:%M %p')

    return render_template('/cards/detail.html', 
                           data=card, 
                           desc_list=desc_list, 
                           views=views,
                           com_list=com_list)

@app.route('/cards/<int:card_id>/add_comment', methods=['POST'])
def add_commment(card_id):
    """ User adds Comment """

    if not g.user:
        flash('Access unauthorized.', 'danger')
        return redirect(url_for('card_show', card_id=card_id))
    
    context = request.form['comment']
    comment = Comment(card_api_id=card_id,
                        user_id=g.user.id,
                        context=context)
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('card_show', card_id=card_id))