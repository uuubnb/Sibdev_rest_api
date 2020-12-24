from rest_framework import permissions
from apps.places.models import Place
from django.http import Http404


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user


class IsPlaceOwnerOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method == 'POST':
            try:
                place = Place.objects.get(id=request.data.get('place'))
            except Place.DoesNotExist:
                return Http404

            return place.owner == request.user
        else:
            return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.place.owner == request.user

