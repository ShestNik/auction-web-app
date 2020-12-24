from .models import Lot, Profile, Category
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth

from django.contrib.auth import models, authenticate, login
from django.template import RequestContext
from django.shortcuts import get_object_or_404
from django.views import generic
from django.forms import ModelChoiceField	
from .timer import LotTimer
from django.urls import reverse_lazy
from .lot_logic import LotLogic, LotLogicException
from .user_logic import UserLogic
from django.http import Http404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import routers, serializers, viewsets
from .serializers import LotSerializer, LotDetailSerializer, CategorySerializer, ProfileSerializer
from rest_framework import status
from django.http import JsonResponse
from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.response import Response
from categorylogic import 

class CategoryApiView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
