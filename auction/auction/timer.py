import threading
from auction.models import Lot, Profile, Category
import auction.models 
from .singleton import Singleton

class LotTimer(metaclass=Singleton):
	timers = dict()
	
	def start(self, lot_id):
		try:
			timer = self.timers[lot_id]
		except KeyError:
			pass
		else:
			self.timers.pop(lot_id)
		finally:
			lot = auction.models.Lot.get(lot_id)
			self.timers[lot_id] = threading.Timer(float(str(lot.timer)), lambda: lot.set_sold())
			timer = self.timers[lot_id]
			timer.start()

	def stop(self, lot_id):
		try:
			timer = self.timers[lot_id]
			timer.cancel()
		except KeyError:
			pass