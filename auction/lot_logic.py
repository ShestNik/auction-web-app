from .models import Lot, Profile, Category
from .timer import LotTimer
from django.shortcuts import get_object_or_404
from django.contrib.auth import models

class LotLogicException(Exception):
    def __init__(self, text):
        self.txt = text

class LotLogic():
	@staticmethod
	def get_by_pk(pk: int):
		try:
			lot = Lot.objects.get(pk=pk)
		except Lot.DoesNotExist:
			raise LotLogicException('Lot does not exists')
		else:
			return lot

	@staticmethod
	def get_all():
		return Lot.objects.all()

	@staticmethod
	def update_price(up_price: float, lot_id: int, user_id: int):
		try:
			lot_inst = get_object_or_404(Lot, pk = lot_id)
		except Exception:
			raise LotLogicException("Objectwith pk=" +str(lot_id) +  "does not exist!")
		if up_price <= 0:
			raise LotLogicException("Up_price should be positive")
		#print(lot_inst.is_sold, lot_inst.dj_owner_id != user_id)
		if not lot_inst.is_sold and lot_inst.dj_owner_id != user_id:
			lt = LotTimer()
			lt.stop(lot_id)
			if(lot_inst.cur_price):
				lot_inst.cur_price += up_price
			else:
				lot_inst.cur_price = lot_inst.start_price + up_price
			lot_inst.cur_customer_id = models.User.objects.get(pk=user_id)
			lot_inst.save()
			lt.start(lot_id)
		elif lot_inst.is_sold:
			raise LotLogicException("Lot is Already sold!")
		elif lot_inst.dj_owner_id == user_id:
			raise LotLogicException("You can't buy your own lot!")

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
		return new_lot
