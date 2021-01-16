from django.test import Client, TestCase
import sys
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

class TestException(Exception):
    def __init__(self, text):
        self.txt = text

class EndToToEnd(TestCase):
    ok = 0
    def setUp(self):
        user = User.objects.create_user('name','name@name.ru', 'aA1!password', )
        user.save()
        category = auction.models.Category(name='1', description='1')
        category.save()

    def test_create_post(self):
        for i in range(100):
            user_data = {
                    'username': 'name', 
                    'email': 'name@name.ru', 
                    'password': 'aA1!password', 
                }

            lot_data = {
                'name': 'e2e_test', 
                'start_price': 1,
                'timer': 1, 
                'category_id': 1,
            }

            #print(login)
            response = self.client.post('/api/v1/api-auth/login', data=user_data, follow=True)
            self.assertEqual(response.status_code, 200)
            login = self.client.login(username= user_data['username'],password=user_data['password'], )
            self.assertTrue(login)
            self.assertEqual(django.contrib.auth.models.User.objects.get(username=user_data['username']).email, user_data['email'])

            response = self.client.post('/api/v1/lots/', data=lot_data)
            self.assertEqual(response.status_code, 201)
            lot = auction.models.Lot.objects.get(pk=i+1)
            self.assertEqual(lot.start_price, lot_data['start_price'])
            self.ok += 1

    def tearDown(self):
        print("passed", self.ok, "tests")

if __name__ == "__main__":
    unittest.main()