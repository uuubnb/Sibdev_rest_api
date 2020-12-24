from rest_framework import serializers
from apps.places.models import Place, Ingredient, Meal


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
            'avg_cost',
            'latitude',
            'longitude',
        )
        read_only_fields = (
            'owner',
        )


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'name',
            'calories',
        )


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = (
            'id',
            'name',
            'place',
            'price',
            'ingredients',
            'total_calories',
        )
        read_only_fields = (
            'total_calories',
        )

