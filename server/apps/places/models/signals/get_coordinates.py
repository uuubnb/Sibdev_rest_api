from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.places.models import Place
from yandex_geocoder import Client
import os


@receiver(post_save, sender=Place)
def get_coordinates(sender, instance, **kwargs):
    if instance.latitude is None:
        YANDEX_KEY = os.getenv('YANDEX_KEY')
        client = Client(YANDEX_KEY)
        coordinates = client.coordinates(instance.address)
        instance.latitude = coordinates[1]
        instance.longitude = coordinates[0]
        instance.save()
