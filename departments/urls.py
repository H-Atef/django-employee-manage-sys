from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register our viewset with it
router = DefaultRouter()
router.register('departments-viewset', views.DepartmentViewSet)

urlpatterns = [
    path('view-all-departments/', views.view_all_departments, name='view_all_departments'),
    path('search-department/<int:dept_id>/', views.view_department_by_id, name='view_department_by_id'),
   
]+router.urls
