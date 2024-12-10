
from . import serializers,models
from django.http import JsonResponse




def viewAlldept(request):
    model=models.Department.objects.all()
    return JsonResponse(serializers.DepartmentSerializer(model,many=True).data,safe=False)
