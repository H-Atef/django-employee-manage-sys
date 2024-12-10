
from rest_framework import serializers
from . import models

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'

    def to_representation(self, instance):
        """
        Customize the representation of the department.
        to control how the fields are represented in the response.
        """
        representation = super().to_representation(instance)
        representation['num_of_employees'] = instance.num_of_employees
        
        return representation