import sys
import os
import unittest
import django
from django.test import Client, TestCase
sys.path.append('/home/kolya/BAUMANKA/7/test and debug/code/auction')
sys.path.append('/home/kolya/BAUMANKA/7/test and debug/code/auction/auction')
#print(sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kursach.settings")
import settings
from django.contrib.auth.models import User
#from mock import patch
import auction.timer
import auction.models
import auction
from auction.lot_logic import LotLogic, LotLogicException
from unittest.mock import patch
import threading

class TestException(Exception):
    def __init__(self, text):
        self.txt = text

class TimerTest(TestCase):
    
    @patch('auction.models.Lot')
    @patch('threading.Timer')
    def test_start(self, MockTimer, MockLot):
        MockLot.get.return_value = auction.models.Lot()
        mock_timer = MockTimer()
        mock_lot = MockLot()
        mock_lot.timer = 0
        t = auction.timer.LotTimer()
        
        t.start(0)
        
        self.assertEqual(len(t.timers), 1)

        mock_timer.start.assert_called_once()

    @patch('threading.Timer')
    def test_stop_ok(self, MockTimer):
        mock_timer = MockTimer()
        t = auction.timer.LotTimer()
        t.timers[0] = threading.Timer(0, lambda: 0)

        t.stop(0)

        mock_timer.cancel.assert_called_once()

if __name__ == "__main__":
    unittest.main()