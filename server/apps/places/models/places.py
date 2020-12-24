from django.db import models
from django.contrib.auth.models import User


class Place(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100
    )
    picture = models.ImageField(
        blank=True,
    )
    time_open = models.TimeField(
        null=True,
        blank=True,
        auto_now=False,
        auto_now_add=False
    )
    time_close = models.TimeField(
        null=True,
        blank=True,
        auto_now=False,
        auto_now_add=False
    )
    address = models.CharField(
        max_length=100
    )
    avg_cost = models.FloatField(
        null=True,
        blank=True,
    )
    latitude = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=7,
    )
    longitude = models.DecimalField(
        null=True,
        blank=True,
        max_digits=10,
        decimal_places=7,
    )

    class Meta:
        verbose_name = 'Название заведения'
        verbose_name_plural = 'Названия заведений'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=100
    )
    calories = models.PositiveSmallIntegerField(
        default=0
    )

    class Meta:
        verbose_name = 'Название ингридиента'
        verbose_name_plural = 'Названия ингридиентов'

    def __str__(self):
        return self.name


class Meal(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE
    )
    name = models.CharField(
        max_length=100
    )
    picture = models.ImageField(
        blank=True
    )
    price = models.DecimalField(
        default=0,
        max_digits=7,
        decimal_places=2,
    )
    ingredients = models.ManyToManyField(
        Ingredient
    )
    total_calories = models.IntegerField(
        default=0
    )

    class Meta:
        verbose_name = 'Название блюда'
        verbose_name_plural = 'Названия блюд'

    def __str__(self):
        return self.name

