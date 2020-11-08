from .models import Lot, Profile, Category
from .timer import LotTimer
from django.shortcuts import get_object_or_404
from django.contrib.auth import models

class LotLogic():

	@staticmethod
	def update_price(up_price: float, lot_id: int, user_id: int):
		print(user_id)
		lt = LotTimer()
		lt.stop(lot_id)
		print(lot_id)
		lot_inst = get_object_or_404(Lot, pk = lot_id)
		if(lot_inst.cur_price):
			lot_inst.cur_price += up_price
		else:
			lot_inst.cur_price = lot_inst.start_price + up_price
		lot_inst.cur_customer_id = models.User.objects.get(pk=user_id)
		lot_inst.save()
		lt.start(lot_id)

	@staticmethod
	def create_lot(form_data: dict, user):
		name = form_data['name']
		start_price = form_data['start_price']
		timer = form_data['timer']
		category_id = form_data['category_id']
		dj_owner_id = models.User.objects.get(username=user)
		print(name, start_price, timer, category_id, dj_owner_id)
		new_lot = Lot(name=name, start_price=start_price, timer=timer, category_id=category_id, dj_owner_id = dj_owner_id)
		print(new_lot.timer)
		new_lot.save()
