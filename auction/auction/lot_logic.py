from auction.models import Lot, Profile, Category
import auction.models
import auction.timer 
from django.shortcuts import get_object_or_404
from django.contrib.auth import models


class LotLogicException(Exception):
    def __init__(self, text):
        self.txt = text

class LotLogic():
	@staticmethod
	def get_by_pk(pk: int):
		try:
			lot = auction.models.Lot.objects.get(pk=pk)
		except auction.models.Lot.DoesNotExist:
			raise LotLogicException('Lot does not exists')
		else:
			return lot

	@staticmethod
	def get_all():
		return auction.models.Lot.objects.all()

	@staticmethod
	def update_price(up_price: float, lot_id: int, user_id: int):
		lot_inst = auction.models.Lot.get(lot_id)
		if up_price <= 0:
			raise LotLogicException("Up_price should be positive")
		#print(lot_inst.sold)
		if not lot_inst.is_sold() and not lot_inst.is_owner(user_id):
			lt = auction.timer.LotTimer()
			lt.stop(lot_id)
			lot_inst.up_price(up_price)
			lot_inst.update_customer(user_id)
			lot_inst.save()
			lt.start(lot_id)
		elif lot_inst.is_sold():
			#print(lot_inst.is_sold())
			raise LotLogicException("Lot is Already sold!")
		elif lot_inst.is_owner(user_id):
			#print(lot_inst.is_owner(user_id))
			raise LotLogicException("You can't buy your own lot!")

	@staticmethod
	def create_lot(form_data: dict, user):
		name = form_data['name']
		start_price = form_data['start_price']
		timer = form_data['timer']
		category_id = form_data['category_id']
		dj_owner_id = models.User.objects.get(username=user)
		#print(name, start_price, timer, category_id, dj_owner_id)
		new_lot = Lot(name=name, start_price=start_price, timer=timer, category_id=category_id, dj_owner_id = dj_owner_id)
		#print(new_lot.timer)
		new_lot.save()
		return new_lot
