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

class CategoryApiView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class ProfileApiView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

class LotApiView(viewsets.ModelViewSet):
    queryset = LotLogic.get_all()
    serializer_class = LotSerializer
    def perform_create(self, serializer):
        serializer.save(dj_owner_id=self.request.user)

class LotDetailApiView(viewsets.ViewSet):
    queryset = LotLogic.get_all()
    serializer_class = LotSerializer
    def list(self, request):
        serializer = LotSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = LotSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(dj_owner_id=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def partial_update(self, request, pk=None):
        queryset = LotLogic.get_by_pk(pk)
        print(request.data)
        response_data = ""
        try:
            LotLogic.update_price(float(request.data["up_price"]), pk, request.user.id)
        except LotLogicException as e:
            response_data = str(e)
            #print("hi",e)
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            serializer = LotSerializer(queryset)
            response_data = serializer.data
            status_code = status.HTTP_200_OK
        finally:
            return Response(response_data, status = status_code)
    #def retrieve(self, request, pk=None):
    #    print('hi')
    #    queryset = LotLogic.get_by_pk(pk)
    #    return LotLogic.get_by_pk(pk)
    #def patch(self, request, pk):
    #    testmodel_object = self.get_object(pk)
    #    serializer = TestModelSerializer(testmodel_object, data=request.data, partial=True) # set partial=True to update a data partially
    #    if serializer.is_valid():
    #        serializer.save()
    #        return JsonResponse(code=201, data=serializer.data)
    #    return JsonResponse(code=400, data="wrong parameters")