from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.TextField()
    last_name = models.TextField()
    date_of_birth = models.DateField(null=True, blank=True)

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    description = models.TextField()

class Lot(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.TextField()
    start_price = models.FloatField()
    cur_price = models.FloatField()

    owner_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True) 
    cur_customer_id = models.ForeignKey('User', on_delete=models.SET_NULL, null=True) 

    category_id = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)