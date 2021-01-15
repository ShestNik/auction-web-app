from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from django.contrib.auth import models	as m
from django.dispatch import receiver
from django.db.models.signals import post_save

class Profile(models.Model):
	id = models.AutoField(primary_key=True)
	user = models.OneToOneField(m.User, on_delete=models.CASCADE, null = True)
	#django_user_id = 
	first_name = models.TextField()
	last_name = models.TextField()
	date_of_birth = models.DateField(null=True, blank=True)
	email = models.TextField(null=True)
	#phone_num = models.TextField(null=True)
	def __str__(self):
		return "%s %s" % (self.first_name, self.last_name)

@receiver(post_save, sender=m.User)
def new_user(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
		instance.profile.save()

class Category(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.TextField()
	description = models.TextField()
	def __str__(self):
		return "%s" % self.name

class Lot(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.TextField()
	start_price = models.FloatField(validators=[MinValueValidator(0.01)])
	cur_price = models.FloatField(null=True)

	timer = models.IntegerField(default=1)

	dj_owner_id = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		null=True,
		related_name="owner"
	)
	cur_customer_id = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		null=True,
		on_delete=models.SET_NULL,
		related_name="customer"
	)
	category_id = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
	
	is_sold = models.BooleanField(default = False, null=True)
	
	def __str__(self):
		return str(self.name)

	def set_sold(self):
		#print('set_sold\n')
		self.is_sold  = True
		self.save()

	def is_already_sold(self, user):
		#print(user, self.dj_owner_id, self.sold == True)
		return user == self.dj_owner_id and self.is_sold == True

	def is_won(self, user):
		#print(user, self.cur_customer_id, self.sold == True)
		return user == self.cur_customer_id and self.is_sold == True
	
	def up_price(self, up_price):
		if(self.cur_price):
			self.cur_price += up_price
		else:
			self.cur_price = self.start_price + up_price
	
	def update_customer(self, user_id):
		self.cur_customer_id = m.User.objects.get(pk=user_id)
	
	def check_sold(self):
		return self.is_sold
	
	def is_owner(self, user_id):
		return self.dj_owner_id == user_id
	
	@classmethod
	def get(cls,pk):
		return cls.objects.get(pk = pk)