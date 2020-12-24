from rest_framework import viewsets
from apps.places.models import Place, Ingredient, Meal
from apps.places.serializers import PlaceSerializer, IngredientSerializer, MealSerializer
from url_filter.integrations.drf import DjangoFilterBackend
from url_filter.filtersets import ModelFilterSet
from rest_framework import permissions
from apps.main.permissions.main import IsOwnerOrReadOnly, IsPlaceOwnerOrReadOnly


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IngredientFilterSet(ModelFilterSet):
    class Meta(object):
        model = Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = IngredientFilterSet
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class MealFilterSet(ModelFilterSet):
    class Meta(object):
        model = Meal


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    filter_backends = [DjangoFilterBackend]
    filter_class = MealFilterSet
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPlaceOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()
        serializer.instance.refresh_from_db()

    def perform_update(self, serializer):
        serializer.save()
        serializer.instance.refresh_from_db()

