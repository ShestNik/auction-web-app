from .models import Lot, Profile, Category
from .lot_logic import LotLogic, LotLogicException
from .serializers import LotDetailSerializer
from rest_framework import status
from django.http import JsonResponse
from rest_framework import generics, permissions, viewsets, mixins
from rest_framework.response import Response

class LotDetailApiView(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    queryset = LotLogic.get_all()
    serializer_class = LotDetailSerializer

    def partial_update(self, request, pk=None):
        queryset = LotLogic.get_by_pk(pk)
        #print(request.data)
        response_data = ""
        try:
            LotLogic.update_price(float(request.data["up_price"]), pk, request.user.id)
        except LotLogicException as e:
            response_data = str(e)
            #print("hi",e)
            status_code = status.HTTP_400_BAD_REQUEST
        else:
            serializer = LotDetailSerializer(queryset)
            response_data = serializer.data
            status_code = status.HTTP_200_OK
        finally:
            return Response(response_data, status = status_code)

    def get_permissions(self):
        permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    #def patch(self, request, pk):
    #    testmodel_object = self.get_object(pk)
    #    serializer = TestModelSerializer(testmodel_object, data=request.data, partial=True) # set partial=True to update a data partially
    #    if serializer.is_valid():
    #        serializer.save()
    #        return JsonResponse(code=201, data=serializer.data)
    #    return JsonResponse(code=400, data="wrong parameters")