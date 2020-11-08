from .models import Lot, Profile, Category
from .timer import LotTimer
from django.shortcuts import get_object_or_404
from django.contrib.auth import models
from django.contrib.auth import models, authenticate, login

class UserLogic():

	@staticmethod
	def create_user(user, form_data: dict):
		user.refresh_from_db()
		user.profile.first_name = form_data['first_name']
		user.profile.last_name = form_data['last_name']
		user.profile.date_of_birth = form_data['date_of_birth']
		user.save()
		return user
	
	@staticmethod
	def auth(user, password, request):
		my_password = password
		user = authenticate(username=user.username, password=my_password)
		login(request, user)