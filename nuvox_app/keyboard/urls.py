from django.urls import path, include
from rest_framework import routers

from .views import keyboard, random_word, DataCollectionSwipeViewSet

router = routers.DefaultRouter()
router.register('data-collection-swipes', DataCollectionSwipeViewSet, 'data-collection-swipes')
urlpatterns = [
    path('', keyboard, name='keyboard'),  # TODO remove this once homepage is implemented.
    path('keyboard/', keyboard, name='keyboard'),
    path('api/', include(router.urls)),
    path('api/random-word/', random_word, name='random-word')
    ]
