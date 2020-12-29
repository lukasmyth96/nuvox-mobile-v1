from django.urls import path

from .views import keyboard

urlpatterns = [
    path('keyboard/', keyboard, name='keyboard'),
    ]
