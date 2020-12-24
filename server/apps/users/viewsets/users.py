from rest_framework import mixins, viewsets
from django.contrib.auth.models import User
from apps.users.serializers import UserSerializer

from drf_yasg import openapi
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema


@method_decorator(name='create', decorator=swagger_auto_schema(
    request_body=UserSerializer,
    responses=
    {
        201: openapi.Response('successfully created user.', openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username'],
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, title='ID', read_only=True),
                'username': openapi.Schema(type=openapi.TYPE_STRING, title='Имя пользователя'),
                'token': openapi.Schema(type=openapi.TYPE_STRING, title='Token', read_only=True),
            },
        )),
    },
))
class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

