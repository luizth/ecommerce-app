from django.urls import path

from .views import get, register, login

urlpatterns = [
    path('users', get),
    path('register', register),
    path('login', login)
]
