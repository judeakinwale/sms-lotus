from django.db import models
from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.HyperlinkedModelSerializer):
    """serializer for the User model"""

    class Meta:
        model = get_user_model()
        fields = ['id', 'url', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 4},
            'url': {'view_name': 'core:user-detail'}
        }

    def create(self, validated_data):
        """create a new user with an encrypted password and return it"""
        return get_user_model().create_user(**validated_data)

    def update(self, instance, validated_data):
        """update a user, set an encrypted password and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
