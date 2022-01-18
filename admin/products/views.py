from rest_framework import generics, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from admin.pagination import CustomPagination
from users.authentication import JWTAuthentication
from .models import Product
from .serializers import ProductSerializer


class ProductGenericAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = CustomPagination

    def get(self, req, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(req, pk).data
            })

        return self.list(req)

    def post(self, req):
        return Response({
            'data': self.create(req).data
        })

    def put(self, req, pk=None):
        return Response({
            'data': self.partial_update(req, pk).data
        })

    def delete(self, req, pk=None):
        return self.destroy(req, pk)
