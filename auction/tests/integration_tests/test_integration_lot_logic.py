from django.test import Client, TestCase
import sys
import os
import django
from django.db import connections
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
        user = User.objects.create_user(username='john',
                                 email='john@john.com',
                                 password='aaaa')
        #user.save()
        user = User.objects.create_user(username='jack',
                                 email='john@john.com',
                                 password='aaaa')
        #user.save()
        record = auction.models.Lot(name = 'test_auct_logic', start_price = 1, timer = 0)
        print(record.id)
        record.save()
        record = auction.models.Lot(name = 'test_auct2_logic', start_price = 1, timer = 2)
        record.save()

    def test_make_bet(self):
        record = auction.models.Lot.objects.get(name='test_auct_logic')
        user = User.objects.get(username='john')

        #LotLogic.update_price(1, record.id, user.id)
        #time.sleep(0.1)
        #record.refresh_from_db()
        #print(record.cur_price, record.is_sold)

        self.assertEqual(record.cur_price, None)


if __name__ == "__main__":
    unittest.main()