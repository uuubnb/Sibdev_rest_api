from rest_framework import serializers
from apps.places.models import Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = (
            'owner',
            'name',
            'picture',
            'time_open',
            'time_close',
            'address',
            'latitude',
            'longitude',
        )
        read_only_fields = (
            'owner',
        )
