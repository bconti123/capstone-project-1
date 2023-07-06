"""User model tests."""

# run these tests like:
#
#    python3 -m unittest test_user_model.py
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
        u1 = User(
            id = 12341234,
            username = 'Yugi',
            password = 'password',
            email = 'Yugi@yugi.com'
        )
        u2 = User(
            id = 3333,
            username = 'Joey',
            password = 'password',
            email = 'Joey@joey.com'
        )

        db.session.add(g1, u1, u2)
        db.session.commit()

        u1 = User.query.get(12341234)
        u2 = User.query.get(3333)
        g1 = User.query.get(2222)

        self.u1 = u1
        self.u2 = u2
        self.g1 = g1

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res