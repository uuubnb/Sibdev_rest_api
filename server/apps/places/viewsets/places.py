from rest_framework import viewsets
from apps.places.models import Place, Ingredient, Meal
from apps.places.serializers import PlaceSerializer, IngredientSerializer, MealSerializer
from apps.places.filters import IngredientFilterSet, MealFilterSet, IngredientFilterBackend, \
    MealFilterBackend, DjangoFilterDescriptionInspector
from rest_framework import permissions
from apps.main.permissions.main import IsOwnerOrReadOnly, IsPlaceOwnerOrReadOnly
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='list', decorator=cache_page(60 * 15))
@method_decorator(name='retrieve', decorator=cache_page(60 * 15))
class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@method_decorator(name='list', decorator=swagger_auto_schema(
    filter_inspectors=[DjangoFilterDescriptionInspector],
    operation_description='''
    Получение списка всех ингридиентов и фильтрация по запросам:
    - по id блюда - отображает все ингридиенты в этом блюде;
    - по количеству калорий - отображает все ингридиенты с указанным количеством калорий 
    '''
))
class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [IngredientFilterBackend]
    filter_class = IngredientFilterSet
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@method_decorator(name='list', decorator=swagger_auto_schema(
    filter_inspectors=[DjangoFilterDescriptionInspector],
    operation_description='''
    Получение списка всех ингридиентов и фильтрация по запросам:
    - по id заведения - отображает все блюда в указанном заведении;
    - по ингридиенту - отображает все блюда с указанным ингридиентом
    '''
))
class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    filter_backends = [MealFilterBackend]
    filter_class = MealFilterSet
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsPlaceOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()
        serializer.instance.refresh_from_db()

    def perform_update(self, serializer):
        serializer.save()
        serializer.instance.refresh_from_db()

