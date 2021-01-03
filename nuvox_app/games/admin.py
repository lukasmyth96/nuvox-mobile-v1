from django.contrib import admin

from games.models import Game


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_on', 'number_of_successful_swipes', 'number_of_unsuccessful_swipes')

    @staticmethod
    def number_of_successful_swipes(obj: Game):
        return len(obj.successful_swipes)

    @staticmethod
    def number_of_unsuccessful_swipes(obj: Game):
        return len(obj.unsuccessful_swipes)
