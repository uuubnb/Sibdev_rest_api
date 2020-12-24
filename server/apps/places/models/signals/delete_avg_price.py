from django.db.models.signals import post_delete
from django.db.models import Avg
from django.dispatch import receiver
from apps.places.models import Meal, Place


@receiver(post_delete, sender=Meal)
def delete_avg_price(sender, instance, **kwargs):
    place = Place.objects.get(id=instance.place_id)
    price = place.meal_set.aggregate(Avg('price'))
    value = price.get('price__avg') or 0
    Place.objects.filter(id=instance.place_id).update(avg_cost=value)

