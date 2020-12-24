from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.places.models import Place
from yandex_geocoder import Client
from yandex_geocoder.exceptions import NothingFound
import logging
import os


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Place)
def get_coordinates(sender, instance, **kwargs):
    if instance.latitude is None:
        try:
            YANDEX_KEY = os.getenv('YANDEX_KEY')
            client = Client(YANDEX_KEY)
            coordinates = client.coordinates(instance.address)
            instance.latitude = coordinates[1]
            instance.longitude = coordinates[0]
            instance.save()
        except NothingFound:
            logger.warning('the address provided by user is wrong')

