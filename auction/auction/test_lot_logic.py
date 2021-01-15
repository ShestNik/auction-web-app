import sys
import os
import unittest
import django
from django.test import Client, TestCase
sys.path.append('/home/kolya/BAUMANKA/7/test and debug/code/auction')
sys.path.append('/home/kolya/BAUMANKA/7/test and debug/code/auction/auction')
#print(sys.path)
import settings
from django.contrib.auth.models import User
#from mock import patch
import auction.timer as timer
import auction.models
from auction.lot_logic import LotLogic, LotLogicException
from unittest.mock import patch

class TestException(Exception):
    def __init__(self, text):
        self.txt = text

class LotTest(TestCase):

    def setUp(self):
        pass
    
    @patch('auction.models.Lot')
    def test_negative_price(self, MockLot):
        MockLot.get_by_pk.return_value = MockLot()
        try:
            LotLogic.update_price(-1, -1, -1)
        except LotLogicException as e:
            print(e)
        else:
            raise TestException("Updated price with negative price")

if __name__ == "__main__":
    unittest.main()