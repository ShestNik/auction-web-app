from . import views
from rest_framework import serializers
from .models import Lot, Profile, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class LotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = '__all__'
        read_only_fields = ("id", "cur_price","timeout","dj_owner_id", "link1", "is_sold", "cur_customer_id")
        
class LotDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lot
        fields = ('name', 'start_price', 'timer', 'is_sold', 'category_id', 'cur_price')
        read_only_fields = ('is_sold',)
    #def 