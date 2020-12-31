from django.contrib import admin

from games.models import Game
from keyboard.models import DataCollectionSwipe


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_on', 'number_of_successful_swipes', 'number_of_unsuccessful_swipes')

    @staticmethod
    def number_of_successful_swipes(obj: Game):
        swipes_for_this_game = DataCollectionSwipe.objects.filter(game=obj, trace_matches_text=True)
        return len(swipes_for_this_game)

    @staticmethod
    def number_of_unsuccessful_swipes(obj: Game):
        swipes_for_this_game = DataCollectionSwipe.objects.filter(game=obj, trace_matches_text=False)
        return len(swipes_for_this_game)
