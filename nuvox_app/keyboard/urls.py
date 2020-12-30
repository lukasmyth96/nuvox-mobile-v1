from django.urls import path, include
from rest_framework import routers

from .views import keyboard, random_word, CollectedSessionViewSet

router = routers.DefaultRouter()
router.register('data-collection-swipes', CollectedSessionViewSet, 'data-collection-swipes')
urlpatterns = [
    path('', include(router.urls)),
    path('keyboard/', keyboard, name='keyboard'),
    path('random-word/', random_word, name='random-word')
    ]
