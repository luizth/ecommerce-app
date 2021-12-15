from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import exceptions

from .serializers import UserSerializer

from .models import User


@api_view(['GET'])
def get(req):
    serializer = UserSerializer(User.objects.all(), many=True)
    return Response(serializer.data)


@api_view(['POST'])
def register(req):
    data = req.data

    if data['password'] != data['password_confirm']:
        raise exceptions.APIException('Passwords do not match.')

    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
def login(req):
    email = req.data.get('email')
    password = req.data.get('password')

    user = User.objects.filter(email=email).first()

    if user is None:
        raise exceptions.AuthenticationFailed('User not found.')

    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Incorrect password.')

    return Response('success')
