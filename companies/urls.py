from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create a router and register the CompanyViewSet
router = DefaultRouter()
router.register('companies-viewset', views.CompanyViewSet)

urlpatterns = [
    path('search-company/<int:company_id>/', views.view_company_by_id, name='view_company_by_id'),
    path('view-all-companies/', views.view_all_companies, name='view_all_companies'),
]+router.urls
