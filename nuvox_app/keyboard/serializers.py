from rest_framework import serializers

from keyboard.models import DataCollectionSwipe


class DataCollectionSwipeSerializer(serializers.ModelSerializer):

    class Meta:
        model = DataCollectionSwipe
        fields = ('target_text', 'trace')
