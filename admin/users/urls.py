from django.urls import path

from .views import get, register

urlpatterns = [
    path('users', get),
    path('register', register),
]
