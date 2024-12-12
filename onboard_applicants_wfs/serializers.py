from rest_framework import serializers
from . import models

class OnBoardingApplicantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OnBoardingApplicant
        fields="__all__"