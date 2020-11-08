from django.shortcuts import render, redirect
from django.views import generic
from django import forms
from .models import Lot, Profile, Category
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django import forms
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import models, authenticate, login
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.views import generic
from django.forms import ModelChoiceField	
from .timer import LotTimer
from django.urls import reverse_lazy
from .lot_logic import LotLogic
from .user_logic import UserLogic

class UpPriceForm(forms.Form):
	up_price = forms.FloatField(min_value=0.01)

class SignUpForm(UserCreationForm):
	first_name = forms.CharField()
	last_name = forms.CharField()
	date_of_birth = forms.DateField()
	class Meta:
		model = models.User
		fields = ('username', 'email', 'first_name','last_name', 'date_of_birth', 'password1', 'password2', )

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user = UserLogic.create_user(user, form.cleaned_data)
			UserLogic.auth(user, form.cleaned_data['password1'], request)
			return redirect('index')
		else:
			form = SignUpForm()
			return render(request, 'registration/signup.html', {'form': form})
	else:
		form = SignUpForm()
		return render(request, 'registration/signup.html', {'form': form})

class CreateLotFormView(ModelForm):
	category_id = ModelChoiceField(queryset=Category.objects.all(), to_field_name='name')

	class Meta:
		model = Lot
		fields = ['name', 'start_price', 'timer', 'category_id', ]
		labels = {
					'name': ('Название'), 
					'start_price': ('Начальная цена'),
					'timer': ('Обратный отсчет'), 
					'category_id': ('Категория'),
				 }
		help_texts = {
						'name': ('Введите название лота\n'), 
						'start_price': ('Введите начальную цену(в рублях)\n'),
						'timer': ('Введите обратный отсчет в секундах\n'), 
						'category_id': ('Выберите категорию\n'),
					 }

def index(request):
	if request.method == 'POST':
		lots = Lot.objects.all()
		form = CreateLotFormView(request.POST)
		if form.is_valid():
			LotLogic.create_lot(form.cleaned_data, request.user)
			return render(request, 'auction/lot_list.html', {'lots': lots, 'form': CreateLotFormView()})
			
	if request.method == 'GET':
		lots = Lot.objects.all()
		form = CreateLotFormView()
		return render(request, 'auction/lot_list.html', {'lots': lots, 'form': form})

@login_required	
def lot_detail_view(request,pk):
	try:
		lot=Lot.objects.get(pk=pk)
	except Lot.DoesNotExist:
		raise Http404("Lot does not exist")
	email = None
	
	if request.method == "POST":
		form = UpPriceForm(request.POST)
		lot_id = int(request.path.split("/")[2])
		if form.is_valid():
			LotLogic.update_price(form.cleaned_data['up_price'], lot_id, request.user.id)
	else:
		form = UpPriceForm(request.POST)
		if lot.is_sold:
			customer = models.User.objects.get(username=request.user)
			email = customer.email
	return render(
		request,
		'auction/lot_detail.html',
		context={'lot':lot,'form':form,'email':email}
	)
