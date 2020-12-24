from .models import Lot, Profile, Category
from .timer import LotTimer

class CategoryLogic():
    @staticmethod
    def get_all():
        return Category.objects.all()