"""View model tests."""

# run these tests like:
#
#    python3 -m unittest -v test_view_model.py
import os
from unittest import TestCase

from models import db, View, User
from sqlalchemy.exc import IntegrityError, NoResultFound

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database
os.environ['DATABASE_URL'] = "postgresql:///yugioh_eff_checker_test"

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data


class ViewModelTestCase(TestCase):
    """ Test Users """

    def setUp(self):
        db.drop_all()
        db.create_all()

        # Create 1 guest user with an specific id
        g1 = User(
            id = 2222
        )

        db.session.add(g1)
        db.session.commit()
        g1 = db.session.get(User, 2222)
        self.g1_id = g1.id
        # Dark Magician's card ID
        self.card_api_id = '46986414'
    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_every_two_hours(self):

        result = View.every_two_hours(self.card_api_id, self.g1_id)
        self.assertEqual(result, None)
    
    def test_seen_card(self):

        result = View.seen_card(self.g1_id, self.card_api_id)
        self.assertEqual(result, None)


        
