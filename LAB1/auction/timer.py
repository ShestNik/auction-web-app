from threading import Timer 
from .models import Lot, Profile, Category
from .singleton import Singleton

class LotTimer(metaclass=Singleton):
	timers = dict()
	
	def start(self, lot_id):
		try:
			timer = self.timers[lot_id]
		except KeyError:
			lot = Lot.objects.get(pk = lot_id)
			self.timers[lot_id] = Timer(float(str(lot.timer)), lambda:	lot.set_sold())
			timer = self.timers[lot_id]
		else:
			self.timers.pop(lot_id)
			lot = Lot.objects.get(pk = lot_id)
			self.timers[lot_id] = Timer(float(str(lot.timer)), lambda: lot.set_sold())
			timer = self.timers[lot_id]
		finally:
			timer.start()
	def stop(self, lot_id):
		try:
			timer = self.timers[lot_id]
			timer.cancel()
		except KeyError:
			lot = Lot.objects.get(pk = lot_id)
			self.timers[lot_id] = Timer(float(str(lot.timer)), lambda: lot.set_sold())