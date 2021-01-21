from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from games.models import Game
from games.serializers import GameSerializer


class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    http_method_names = ['get', 'post']
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@require_http_methods(['GET'])
def leaderboard(request):
    """Returns list of dicts containing user (username) and score
    for top n entrants."""
    games = list(Game.objects.all())
    games.sort(key=lambda game: len(game.successful_swipes), reverse=True)
    top_games = games[:10]
    response = [{'user': game.user.username, 'score': len(game.successful_swipes)} for game in top_games]
    return JsonResponse(response, safe=False)
