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
from  auction.models import Profile, Category, Lot
from django.contrib.auth.models import User
from django.contrib.auth import models

class TestException(Exception):
    def __init__(self, text):
        self.txt = text

class LotTest(TestCase):

    def setUp(self):
        User.objects.create_user(username='john',
                                 email='john@john.com',
                                 password='aaaa')
        User.objects.create_user(username='jack',
                                 email='john@john.com',
                                 password='aaaa')
        record = Lot(name = 'test__1', start_price = 1)
        record.save()
        record = Lot(name = 'test__2', start_price = 1)
        record.save()


    def test_create_none_name(self):
        name = None
        price = 3
        try:
            record = Lot(name = name, start_price = price)
            record.save()
        except:
            pass
        else:
            raise TestException("Model Integrity Error: created category with name None")

    def test_set_sold(self):
        record = Lot.objects.get(name='test__1')
        record.set_sold()
        self.assertEqual(record.is_sold, True)

    def test_get_from_db(self):
        name = 'test__1'
        start_price = 1
        test_record = Lot.objects.get(name=name)
        self.assertEqual(test_record.start_price, start_price)

    def test_str(self):
        name = 'Мебель'
        price = 1
        record = Lot(name = name, start_price = price)

        check_str = str(record)

        self.assertEqual(name, check_str)

    def test_sold_true(self):
        name = 'Мебель'
        price = 1
        user = models.User.objects.get(username='john')
        record = Lot(name=name, start_price = price, dj_owner_id=user, is_sold = True)
        self.assertEqual(record.is_already_sold(user), True)

    def test_sold_wrong_user(self):
        name = 'Мебель'
        price = 1
        user = models.User.objects.get(username='jack')
        user1 = models.User.objects.get(username='john')
        record = Lot(name=name, start_price = price, dj_owner_id=user, is_sold = True)
        self.assertEqual(record.is_already_sold(user1), False)

    def test_sold_not_sold(self):
        name = 'Мебель'
        price = 1
        user = models.User.objects.get(username='jack')
        record = Lot(name=name, start_price = price, dj_owner_id=user, is_sold =False)
        self.assertEqual(record.is_already_sold(user), False)

    def test_is_won_true(self):
        name = 'Мебель'
        price = 1
        user = models.User.objects.get(username='john')
        record = Lot(name=name, start_price = price, cur_customer_id=user, is_sold = True)
        
        res = record.is_won(user)

        self.assertEqual(res, True)

    def test_is_won_wrong_user(self):
        name = 'Мебель'
        price = 1
        user = models.User.objects.get(username='jack')
        user1 = models.User.objects.get(username='john')
        record = Lot(name=name, start_price = price, cur_customer_id=user, is_sold = True)
        
        res = record.is_won(user1)

        self.assertEqual(res, False)

    def test_is_won_not_sold(self):
        name = 'Мебель'
        price = 1
        user = models.User.objects.get(username='jack')
        record = Lot(name=name, start_price = price, cur_customer_id=user, is_sold =False)
        
        res = record.is_won(user)

        self.assertEqual(res, False)

if __name__ == "__main__":
    unittest.main()