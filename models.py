from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

date_today = datetime().now.strftime("%Y-%m-%d %H:%M:%S")

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
    username = db.Column(db.Text, nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    isGuest = db.Column(db.Boolean, default=True)

    comments = db.relationship("Comment", backref='user', cascade="all, delete-orphan")

    def __repr__(self):
        if self.isGuest:
            return f'#{self.id}: Guest'
        else:
            return f'User #{self.id}: {self.username}'

    @classmethod
    def signup(cls, id, username, password):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        User(
        id = id,
        username = username,
        password = hashed_pwd,
        isGuest = False)

        db.session.commit()
        return f'User ID: {id} - {username} was created!'

    @classmethod
    def authenticate(cls, username, password):

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
            
        return False
        
class Card(db.Model):
    """ Card """
    __tablename__ = 'cards'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)

class View(db.Model):
    """ View """
    __tablename__ = 'views'
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=date_today)

class Comment(db.Model):
    """ Comment """
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    context = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=date_today)
