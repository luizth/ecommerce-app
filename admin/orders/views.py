from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from admin.pagination import CustomPagination
from rest_framework.views import APIView
from users.authentication import JWTAuthentication
from .models import OrderItem, Order
from .serializers import OrderSerializer


class OrderGenericAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = CustomPagination

    def get(self, req, pk=None):
        if pk:
            return Response({
                'data': self.retrieve(req, pk).data
            })

        return self.list(req)
