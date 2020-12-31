from rest_framework import serializers

from keyboard.models import DataCollectionSwipe


class DataCollectionSwipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataCollectionSwipe
        fields = ('game', 'target_text', 'trace', 'trace_matches_text')
        read_only_fields = ('trace_matches_text',)
