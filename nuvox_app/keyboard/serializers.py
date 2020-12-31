from rest_framework import serializers

from keyboard.models import DataCollectionSwipe
from keyboard.validators import validate_trace_matches_target_text


class DataCollectionSwipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataCollectionSwipe
        fields = ('target_text', 'trace', 'is_trace_valid')
        read_only_fields = ('is_trace_valid',)

    def validate(self, data):
        validate_trace_matches_target_text(trace=data['trace'], target_text=data['target_text'])
        return data
