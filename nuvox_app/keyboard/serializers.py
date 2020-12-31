from rest_framework import serializers

from keyboard.models import DataCollectionSwipe
from keyboard.validators import validate_trace_matches_target_text


class DataCollectionSwipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataCollectionSwipe
        fields = ('target_text', 'trace', 'trace_matches_text')
        read_only_fields = ('trace_matches_text',)
