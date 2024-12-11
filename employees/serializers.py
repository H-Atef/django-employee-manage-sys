from rest_framework import serializers
from . import models


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        exclude = ['id'] 


    def validate(self, data):
        # Ensure the department belongs to the selected company
        if data['department'].company != data['company']:
            raise serializers.ValidationError("Department must belong to the selected company.")
        return data
    
    def to_representation(self, instance):
        # Custom logic for adding computed properties
        representation = super().to_representation(instance)
        representation['days_employed'] = instance.days_employed
        return representation
