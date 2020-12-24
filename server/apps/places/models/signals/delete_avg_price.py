from django.db.models.signals import post_delete
from django.db.models import Avg
from django.dispatch import receiver
from apps.places.models import Meal, Place


@receiver(post_delete, sender=Meal)
def delete_avg_price(sender, instance, **kwargs):
    qs = Meal.objects.filter(place__id=instance.place.id).aggregate(Avg('price'))
    value = qs.get('price__avg') or 0
    Place.objects.filter(id=instance.place.id).update(avg_cost=value)

