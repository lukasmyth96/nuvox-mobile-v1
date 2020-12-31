from rest_framework import serializers

from keyboard.models import DataCollectionSwipe


class DataCollectionSwipeSerializer(serializers.ModelSerializer):
    game_expired = serializers.SerializerMethodField()

    class Meta:
        model = DataCollectionSwipe
        fields = ('game', 'target_text', 'trace', 'trace_matches_text')
        read_only_fields = ('trace_matches_text',)

    @staticmethod
    def get_game_expired(obj: DataCollectionSwipe):
        """Method for 'game_expired' method field."""
        return obj.game.has_expired
