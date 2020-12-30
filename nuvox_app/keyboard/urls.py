from django.urls import path

from .views import keyboard, random_word

urlpatterns = [
    path('keyboard/', keyboard, name='keyboard'),
    path('random-word/', random_word, name='random-word')
    ]
