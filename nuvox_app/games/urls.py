from django.urls import path, include
from rest_framework import routers

from games.views import GameViewSet

router = routers.DefaultRouter()
router.register('games', GameViewSet, 'games')
urlpatterns = [
    path('api/', include(router.urls)),
]
