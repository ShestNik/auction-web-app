from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
   path('', views.index, name='lot_list'),
   url('index', views.index, name='index'),
   url(r'^lot/(?P<pk>\d+)$', views.lot_detail_view, name='lot-detail'),
   path('accounts/', include('django.contrib.auth.urls')),
   url('accounts/register/', views.signup),
]