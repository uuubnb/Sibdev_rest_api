import coreapi
import coreschema
from apps.places.models import Ingredient, Meal
from url_filter.filtersets import ModelFilterSet
from url_filter.integrations.drf_coreapi import CoreAPIURLFilterBackend
from drf_yasg.inspectors.query import CoreAPICompatInspector
from drf_yasg.inspectors import NotHandled


class IngredientFilterSet(ModelFilterSet):
    class Meta(object):
        model = Ingredient


class MealFilterSet(ModelFilterSet):
    class Meta(object):
        model = Meal


class IngredientFilterBackend(CoreAPIURLFilterBackend):
    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(
                name="meal",
                description="show ingredients in specified meal",
                required=False,
                location='query',
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                name="calories",
                description="show ingredients with specified number of calories",
                required=False,
                location='query',
                schema=coreschema.Integer()
            )]

        return fields


class MealFilterBackend(CoreAPIURLFilterBackend):
    def get_schema_fields(self, view):
        fields = [
            coreapi.Field(
                name="place",
                description="show meals in specified place",
                required=False,
                location='query',
                schema=coreschema.Integer()
            ),
            coreapi.Field(
                name="ingredients",
                description="show meals with specified ingredients",
                required=False,
                location='query',
                schema=coreschema.Integer()
            )]

        return fields


class DjangoFilterDescriptionInspector(CoreAPICompatInspector):
    def get_filter_parameters(self, filter_backend):
        if isinstance(filter_backend, CoreAPIURLFilterBackend):
            result = super(DjangoFilterDescriptionInspector, self).get_filter_parameters(filter_backend)
            for param in result:
                if not param.get('description', ''):
                    param.description = "Filter the returned list by {field_name}".format(field_name=param.name)

            return result

        return NotHandled

