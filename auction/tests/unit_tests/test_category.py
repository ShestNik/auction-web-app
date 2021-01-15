import sys
import os
import unittest
import django
from django.test import Client, TestCase
from category_builder import CategoryBuilder
sys.path.append('/home/kolya/BAUMANKA/7/test and debug/code/auction')
sys.path.append('/home/kolya/BAUMANKA/7/test and debug/code/auction/auction')
#print(sys.path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kursach.settings")
import settings
from auction.models import Profile, Category, Lot

class TestException(Exception):
    def __init__(self, text):
        self.txt = text

class CategoryTest(TestCase):
    def setUp(self):
        cat_builder =  CategoryBuilder()
        cat_builder.with_name('test')
        cat_builder.with_description('_test_')
        record = cat_builder.build()
        record.save()
        
    def test_create_none_name(self):
        cat_builder =  CategoryBuilder()
        cat_builder.with_description('_test_')

        with self.assertRaises(django.db.utils.IntegrityError):
            record = cat_builder.build()
            record.save()


    def test_create_none_descr(self):
        cat_builder =  CategoryBuilder()
        cat_builder.with_name('test')
        record = cat_builder.build()

        with self.assertRaises(django.db.utils.IntegrityError):
            record = cat_builder.build()
            record.save()

    def test_get_from_db(self):
        name = 'test'
        description = '_test_'
        test_record = Category.objects.get(name=name)
        self.assertEqual(test_record.description, description)

    def test_str(self):
        name = 'test'
        cat_builder =  CategoryBuilder()
        cat_builder.with_name(name)
        cat_builder.with_description('_test_')
        record = cat_builder.build()

        check_str = str(record)

        self.assertEqual(name, check_str)

if __name__ == "__main__":
    unittest.main()