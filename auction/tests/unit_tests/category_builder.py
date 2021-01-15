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
from auction.models import Category

class CategoryBuilder():
    name = None
    description = None

    def with_name(self, name: str):
        self.name = name

    def with_description(self, description: str):
        self.description = description
    
    def build(self):
        return Category(name = self.name, description = self.description)