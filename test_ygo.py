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
        id = 46986414
        find = find_card_id(id)
        card_id = find[0]['id']

        self.assertEqual(card_id, id)
        
    def test_find_card_desc(self):
        card = find_card_id(40737112)
        desc_list = find_card_desc(card)
        found_cond = any('condition' in desc for desc in desc_list)
        found_cost = any('cost' in desc for desc in desc_list)
        found_act = any('act' in desc for desc in desc_list)
        self.assertTrue(found_cond)
        self.assertTrue(found_cost)
        self.assertTrue(found_act)





        