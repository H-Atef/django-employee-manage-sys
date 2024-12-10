from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
path("view-all-departments/",views.viewAlldept,name="view-all-departments")
]
