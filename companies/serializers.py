
from rest_framework import serializers
from . import models

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Company
        fields = '__all__'

    def to_representation(self, instance):
        # Custom logic for adding computed properties
        representation = super().to_representation(instance)
        representation['num_of_departments'] = instance.num_of_departments
        representation['num_of_employess'] = instance.num_of_employess
        return representation