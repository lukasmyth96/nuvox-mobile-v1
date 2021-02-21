from django.urls import path, include
from rest_framework import routers

from .views import home, keyboard, game, random_word, DataCollectionSwipeViewSet

router = routers.DefaultRouter()
router.register('data-collection-swipes', DataCollectionSwipeViewSet, 'data-collection-swipes')
urlpatterns = [
    path('', home, name='home'),
    path('keyboard/', keyboard, name='keyboard'),
    path('game/', game, name='game'),
    path('api/', include(router.urls)),
    path('api/random-word/', random_word, name='random-word')
    ]
