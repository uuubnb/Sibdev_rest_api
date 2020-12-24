from django.contrib import admin

from apps.places.models import Place


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'owner',
    )
    readonly_fields = (
        'latitude', 'longitude',
    )
