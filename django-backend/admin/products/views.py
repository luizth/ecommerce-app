from django.core.files.storage import default_storage
from rest_framework import generics, mixins, status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from admin.pagination import CustomPagination
from rest_framework.views import APIView
from users.authentication import JWTAuthentication
from users.permissions import ViewPermissions
from .models import Product
from .serializers import ProductSerializer


class ProductGenericAPIView(
    generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
    mixins.UpdateModelMixin, mixins.DestroyModelMixin
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated & ViewPermissions]
    permissions_object = 'products'
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


class FileUploadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, )

    def post(self, req):
        file = req.FILES['image']
        file_name = default_storage.save(file.name, file)
        url = default_storage.url(file_name)

        return Response({
            'url': 'http://localhost:8000/api' + url
        })
