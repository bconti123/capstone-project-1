# run these tests like:
#
#    python3 -m unittest -v test_ygo.py
from ygo import *
import time

from unittest import TestCase

class Ygo_Cards_TestCase(TestCase):

    def setUp(self):

        self.DMcard = "Dark Magician"
        self.cards = search_card(self.DMcard)
        time.sleep(0.5)
    
    def test_search_card(self):  
        name_list = [card['name'] for card in self.cards]

        self.assertIsInstance(self.cards, list)
        self.assertEqual(self.cards[0]['name'], self.DMcard)
        self.assertIn(self.DMcard, name_list)
        self.assertIn("Dark Magician Girl", name_list)

        

    def test_find_card_id(self):

        id_list = [{card['id'] : card['name'}] for card in self.cards]

        find_card_id()


        