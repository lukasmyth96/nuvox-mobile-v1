from django.contrib import admin

from games.models import Game
from keyboard.models import DataCollectionSwipe


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_on', 'number_of_swipes')

    @staticmethod
    def number_of_swipes(obj: Game):
        swipes_for_this_game = Game.objects.filter(game=obj)
        return len(swipes_for_this_game)
