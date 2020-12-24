from apps.places.models import Place, Meal
from django.db.models.signals import post_save
from django.db.models import Avg
from django.dispatch import receiver


@receiver(post_save, sender=Meal)
def add_avg_price(sender, instance, **kwargs):
    place = Place.objects.get(id=instance.place_id)
    price = place.meal_set.aggregate(Avg('price'))
    value = price.get('price__avg')
    Place.objects.filter(id=instance.place_id).update(avg_cost=value)

