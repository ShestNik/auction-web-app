from .models import Lot, Profile, Category
from .serializers import CategorySerializer
from rest_framework import generics, permissions, viewsets, mixins
from .categorylogic import CategoryLogic 

class CategoryApiView(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = CategorySerializer
    queryset = CategoryLogic.get_all()
    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]
