from rest_framework import viewsets
from apps.places.models import Place
from apps.places.serializers import PlaceSerializer


class PlaceViewSet(viewsets.ModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
