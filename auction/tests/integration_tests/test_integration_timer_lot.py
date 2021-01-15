from django.test import Client, TestCase
import sys
import os
import unittest
import django
sys.path.append('/home/kolya/BAUMANKA/7/test and debug/code/auction')
sys.path.append('/home/kolya/BAUMANKA/7/test and debug/code/auction/auction')
#print(sys.path)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kursach.settings")
import settings
from django.contrib.auth.models import User
#from mock import patch
import auction.timer
import time
import auction.models
from auction.lot_logic import LotLogic, LotLogicException
from unittest.mock import patch

class TestException(Exception):
    def __init__(self, text):
        self.txt = text

class TimerLotIntegrationTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='john',
                                 email='john@john.com',
                                 password='aaaa')
        User.objects.create_user(username='jack',
                                 email='john@john.com',
                                 password='aaaa')
        record = auction.models.Lot(name = 'test_1', start_price = 1, timer = 0)
        record.save()
        record = auction.models.Lot(name = 'test_2', start_price = 1, timer = 2)
        record.save()

    def test_start(self):
        


if __name__ == "__main__":
    unittest.main()