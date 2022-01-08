from rest_framework import exceptions, viewsets, status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .authentication import generate_access_token, JWTAuthentication
from .models import User, Permission, Role
from .serializers import UserSerializer, PermissionSerializer, RoleSerializer

from .lib.utils.logger import Logger


# NOT BEEING USED
@api_view(['GET'])
def users(req):
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

    response = Response()
    token = generate_access_token(user)
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'jwt': token
    }
    return response


@api_view(['POST'])
def logout(_):
    response = Response()
    response.delete_cookie(key='jwt')
    response.data = {
        'message': 'Success'
    }
    return response


class AuthenticatedUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, req):
        serializer = UserSerializer(req.user)

        return Response({
            'data': serializer.data
        })


class PermissionAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, _):
        serializer = PermissionSerializer(Permission.objects.all(), many=True)

        return Response({
            'data': serializer.data
        })


class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, _):
        serializer = RoleSerializer(Role.objects.all(), many=True)

        return Response({
            'data': serializer.data
        })

    def create(self, req):
        serializer = RoleSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


    def retreive(self, _, pk=None):
        role = Role.objects.get(pk=pk)
        serializer = RoleSerializer(role)

        return Response({
            'data': serializer.data
        })

    def update(self, req, pk=None):
        role = Role.objects.get(pk=pk)
        serializer = RoleSerializer(instance=role, data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'data': serializer.data
        }, status=status.HTTP_202_ACCEPTED)

    def destroy(self, req, pk=None):
        role = Role.objects.get(pk=pk)
        role.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
