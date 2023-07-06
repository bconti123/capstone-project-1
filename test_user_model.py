"""User model tests."""

# run these tests like:
#
#    python3 -m unittest -v test_user_model.py
import os
from unittest import TestCase

from models import db, User
from sqlalchemy.exc import IntegrityError

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database
os.environ['DATABASE_URL'] = "postgresql:///yugioh_eff_checker_test"

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data
db.drop_all()
class UserModelTestCase(TestCase):
    """ Test Users """

    def setUp(self):
        """ Create test client, add sample data """
        # Clear DB and Create Fresh DB
        db.drop_all()
        db.create_all()

        # Create 5 guest users
        for i in range(0, 5):
            User.guest_visit()
        # Create 1 guest user with an specific id
        g1 = User(
            id = 2222
        )
        # Create 2 users with an specific informations
        u1 = User.signup(
            1,
            'Yugi',
            'password',
            'Yugi@yugi.com',
        )

        u2 = User.signup(
            2,
            'Joey',
            'password',
            'Joey@joey.com',
        )
 

        db.session.add(g1)
        db.session.commit()


        u1 = db.session.get(User, 1)
        u2 = db.session.get(User, 2)
        g1 = db.session.get(User, 2222)
        self.u1 = u1
        self.u2 = u2
        self.g1 = g1

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_guest_created(self):
        
        g = User.guest_visit()
        self.assertTrue(g.isGuest)

    def test_guest_repr(self):

        expected_repr = f'<#{self.g1.id}: Guest>'
        self.assertEqual(repr(self.g1), expected_repr)
    
    def test_user_repr(self):

        expected_repr = f'<User #{self.u1.id}: {self.u1.username}>'
        self.assertEqual(repr(self.u1), expected_repr)
    
    def test_user_sign_up_success(self):
        
        u = User.signup(self.g1.id, 'Kaiba', 'password', 'Kaiba@KC.com')
        self.assertEqual(u.username, 'Kaiba')
        self.assertEqual(u.email, 'Kaiba@KC.com')

    def test_user_sign_up_fail(self):
        with self.assertRaises(IntegrityError):
            User.signup(self.g1.id, 'Yugi', 'password', 'Atem@Yugi.com')

    def test_user_sign_up_fail_password(self):
        with self.assertRaises(ValueError):
            User.signup(self.g1.id, 'Kaiba', '', 'Kaiba@KC.com')
    
    def test_user_authenticate_success(self):
        self.assertTrue(User.authenticate('Yugi', 'password'))
    
    def test_user_authenticate_username_fail(self):
        self.assertFalse(User.authenticate('Fake', 'password'))

    def test_user_authenticate_password_fail(self):
        self.assertFalse(User.authenticate('Yugi', 'PWD'))
