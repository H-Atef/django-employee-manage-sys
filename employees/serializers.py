from rest_framework import serializers
from . import models


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'

    # def validate(self, data):
    #     # Ensure the department belongs to the selected company
    #     if data['department'].company != data['company']:
    #         raise serializers.ValidationError("Department must belong to the selected company.")
    #     return data
