from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password',)
        write_only_fields = ('password',)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['password'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
