from rest_framework import mixins, viewsets
from django.contrib.auth.models import User
from apps.users.serializers import UserSerializer


class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
