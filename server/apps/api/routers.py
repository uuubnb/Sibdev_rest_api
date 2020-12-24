from rest_framework import routers

from apps.test.viewsets import TestViewSet
from apps.users.viewsets import UserViewSet
from apps.places.viewsets import PlaceViewSet, IngredientViewSet, MealViewSet

router = routers.DefaultRouter()
router.register('test', TestViewSet, basename='test')
router.register('users', UserViewSet, basename='users')
router.register('places', PlaceViewSet, basename='places')
router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('meals', MealViewSet, basename='meals')

