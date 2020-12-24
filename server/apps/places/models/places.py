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
    picture = models.URLField(
        blank=True,
        max_length=200
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

    def __str__(self):
        return self.name
