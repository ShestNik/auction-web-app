from django.test import Client, TestCase
from django.db import connections
import sys
import threading
import os
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
from django.db import connections

class TestException(Exception):
    def __init__(self, text):
        self.txt = text

class TimerLotIntegrationTest(TestCase):
    def setUp(self):
        User.objects.create_user(id=1, username='john',
                                 email='john@john.com',
                                 password='aaaa')
        User.objects.create_user(id=2,username='jack',
                                 email='john@john.com',
                                 password='aaaa')
        record = auction.models.Lot(name = 'test_auct', start_price = 1, timer = 0)
        record.save()
        record = auction.models.Lot(name = 'test_auct2', start_price = 1, timer = 2)
        record.save()

    def test_start(self):
        record = auction.models.Lot.objects.get(name='test_auct')
        timer = auction.timer.LotTimer()
        timer.start(record.id)
        time.sleep(0.1)
        record.refresh_from_db()
        self.assertEqual(record.is_sold, False)

    def test_stop(self):
        record = auction.models.Lot.objects.get(name='test_auct2')
        timer = auction.timer.LotTimer()
        
        timer.start(record.id)
        timer.stop(record.id)
        
        record.refresh_from_db()
        self.assertEqual(record.is_sold, False)
        print(threading.active_count())
        

if __name__ == "__main__":
    unittest.main()