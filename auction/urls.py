from django.urls import path, include
from . import views
from django.conf.urls import url
from rest_framework import routers
from .apiviews import LotApiView, LotDetailApiView, CategoryApiView, ProfileApiView


from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

router = routers.DefaultRouter()
router.register(r'^/lot', LotDetailApiView, basename='Lot')
router.register(r'^/category', CategoryApiView, basename='Category')
#router.register(r'^/profile', ProfileApiView, basename='Profile')
#router.register(r'^lot/{pk}/$', LotDetailApiView,  basename='Lot')


urlpatterns = [
   path('', views.index, name='lot_list'),
   path('api-token-auth/', obtain_jwt_token),
   path('api-token-refresh/', refresh_jwt_token),
   path('api-token-verify/', verify_jwt_token),
   path('api-auth/', include('rest_framework.urls')),
   path('api/v1/register', include('rest_registration.api.urls')),
   url('index', views.index, name='index'),
   url(r'^lot/(?P<pk>\d+)$', views.lot_detail_view, name='lot-detail'),
   path('accounts/', include('django.contrib.auth.urls')),
   url('accounts/register/', views.signup),
   path('api/v1', include(router.urls)),
]
