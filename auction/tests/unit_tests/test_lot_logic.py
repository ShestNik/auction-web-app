import sys
import os
import unittest
import django
from django.test import Client, TestCase
#print(sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kursach.settings")
import settings
from django.contrib.auth.models import User
#from mock import patch
import auction.timer
import auction.models
from auction.lot_logic import LotLogic, LotLogicException
from unittest.mock import patch

class TestException(Exception):
    def __init__(self, text):
        self.txt = text

class LotLogicTest(TestCase):
    
    @patch('auction.models.Lot')
    def test_negative_price(self, MockLot):
        up_price = -1
        lot_id = -1
        user_id = -1
        e = LotLogicException("")

        with self.assertRaises(LotLogicException) as error:
            LotLogic.update_price(up_price, lot_id, user_id)
        
        e = error.exception
        self.assertEqual(e.txt, "Up_price should be positive")

    @patch('auction.models.Lot')
    def test_sold(self, MockLot):
        up_price = 1
        lot_id = -1
        user_id = -1        
        MockLot.get.return_value = auction.models.Lot()
        lot = MockLot()
        lot.is_sold.return_value = True
        lot.is_owner.return_value = True
        e = LotLogicException("")
        
        with self.assertRaises(LotLogicException) as error:
            LotLogic.update_price(up_price, lot_id, user_id)
        
        e = error.exception     
        self.assertEqual(e.txt, "Lot is Already sold!")

    @patch('auction.models.Lot')
    def test_is_owner(self, MockLot):
        up_price = 1
        lot_id = -1
        user_id = -1
        lot = MockLot()
        MockLot.get.return_value = auction.models.Lot()
        lot.check_sold.return_value = False
        lot.is_owner.return_value = True
        e = LotLogicException("")

        with self.assertRaises(LotLogicException) as error:
            LotLogic.update_price(up_price, lot_id, user_id)
        
        e = error.exception
        self.assertEqual(e.txt, "You can't buy your own lot!")

    @patch('auction.models.Lot')
    @patch('auction.timer.LotTimer')
    def test_up_price_ok(self, MockTimer, MockLot):
        up_price = 1
        lot_id = -1
        user_id = -1
        lot = MockLot()
        timer = MockTimer()
        MockLot.get.return_value = auction.models.Lot()
        lot.check_sold.return_value = False
        lot.is_owner.return_value = False
        lot.get.return_value = auction.models.Lot()
        
        LotLogic.update_price(up_price, lot_id, user_id)
        
        timer.stop.assert_called_once()
        timer.start.assert_called_once()
        lot.up_price.assert_called_once()
        lot.update_customer.assert_called_once()
        lot.save.assert_called_once()

if __name__ == "__main__":
    unittest.main()