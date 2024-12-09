
from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.UserInfo
        fields=['user','role']

    def create(self, validated_data):
        # Create user and hash password
        user = models.UserInfo.objects.create(**validated_data)
        return user
        


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username','password','email']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    