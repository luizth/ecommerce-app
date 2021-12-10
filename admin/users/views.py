from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import APIException

from .models import User
from .serializers import UserSerializer


@api_view(['GET'])
def get(req):
    users = User.objects.all()
    return Response(users)


@api_view(['POST'])
def register(req):
    data = req.data

    if data['password'] != data['password_confirm']:
        raise APIException('Passwords do not match.')

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
