from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from sqlalchemy import text
from sqlalchemy.exc import NoResultFound, IntegrityError

date_today = datetime.today()

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask App"""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """ User """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True)
    password = db.Column(db.Text)
    email = db.Column(db.Text, unique=True)
    isGuest = db.Column(db.Boolean, default=True)

    comments = db.relationship("Comment", backref='user', cascade="all, delete-orphan")
    # favorites = db.relationship("Favorite", backref='user', cascade="all, delete-orphan")


    def __repr__(self):
        if self.isGuest:
            return f"<#{self.id}: Guest>"
        else:
            return f"<User #{self.id}: {self.username}>"
        
    @classmethod
    def guest_visit(cls):
        guest = User()
        db.session.add(guest)
        db.session.commit()
        return guest
    
    @classmethod
    def signup(cls, id, username, password, email):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = db.session.get(User, id)

        user.username = username,
        user.password = hashed_pwd,
        user.email = email,
        user.isGuest = False

        db.session.commit()
        return user

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
            
        return False

class View(db.Model):
    """ View """
    __tablename__ = 'views'
    id = db.Column(db.Integer, primary_key=True)
    card_api_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=date_today)


    @classmethod
    def every_two_hours(cls, user_id, card_api_id):
        try:
            query = text('''SELECT * FROM views
                        WHERE user_id= :user_id
                        AND card_api_id = :card_api_id
                        ORDER BY created_at DESC
                        LIMIT 1''')
            result = db.session.execute(query, 
                                        {'user_id':user_id, 
                                        'card_api_id':card_api_id})
            row = result.fetchone()
            if row is not None:
                two_h = row.created_at
                return two_h
        except NoResultFound:
            db.session.rollback()
            raise
    
    @classmethod
    def seen_card(cls, user_id, card_api_id):
        try:
            two_h = cls.every_two_hours(user_id, card_api_id)
            if two_h is None or datetime.now() - two_h > timedelta(hours=2):
                seen = View(card_api_id=card_api_id,
                            user_id=user_id)
                
                db.session.add(seen)
                db.session.commit()
            else:
                pass
        except NoResultFound:
            try:
                seen = View(card_api_id=card_api_id,
                            user_id=user_id)
                db.session.add(seen)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                raise


class Comment(db.Model):
    """ Comment """
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    card_api_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    context = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=date_today)

# class Favorite(db.Model):
#     """ User's favorite card """
#     __tablename__ = 'favorites'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     card_api_id = db.Column(db.Integer, nullable=False)
