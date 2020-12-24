from django.db.models.signals import m2m_changed
from django.db.models import Sum
from django.dispatch import receiver
from apps.places.models import Meal


@receiver(m2m_changed, sender=Meal.ingredients.through)
def get_total_calories(sender, instance, action, **kwargs):
    if action in ["post_add", "post_remove"]:
        qs = Meal.objects.filter(id=instance.id)
        summ = qs.aggregate(Sum('ingredients__calories'))
        value = summ.get('ingredients__calories__sum') or 0
        qs.update(total_calories=value)

