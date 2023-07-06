from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

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

    def __repr__(self):
        if self.isGuest:
            return f'#{self.id}: Guest'
        else:
            return f'User #{self.id}: {self.username}'
    @classmethod
    def guest_visit(cls):
        db.session.add(User())
        db.session.commit()
        return f'Guest created'
    
    @classmethod
    def signup(cls, id, username, password, email):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = User.query.get(id)

        user.username = username,
        user.password = hashed_pwd,
        user.email = email,
        user.isGuest = False

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

class Images(db.Model):
    """ Image """
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    card_api_id = db.Column(db.Integer, nullable=False)
    filename = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.Text, nullable=False)

class View(db.Model):
    """ View """
    __tablename__ = 'views'
    id = db.Column(db.Integer, primary_key=True)
    # card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    card_api_id = db.Column(db.Integer, nullable=False)
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
