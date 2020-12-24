from django.db.models.signals import post_save
from django.db.models import Avg
from django.dispatch import receiver
from apps.places.models import Meal, Place


@receiver(post_save, sender=Meal)
def add_avg_price(sender, instance, **kwargs):
    qs = Meal.objects.filter(place__id=instance.place.id).aggregate(Avg('price'))
    value = qs.get('price__avg')
    Place.objects.filter(id=instance.place.id).update(avg_cost=value)

