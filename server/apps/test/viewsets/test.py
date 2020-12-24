from rest_framework import mixins
from rest_framework import viewsets

from apps.test.models import Test
from apps.test.serializers import TestSerializer


class TestViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = TestSerializer
    queryset = Test.objects.all()
    swagger_schema = None

