from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from games.models import Game
from games.serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    http_method_names = ['post']
    # permission_classes = [IsAuthenticated]  # TODO uncomment after testing
