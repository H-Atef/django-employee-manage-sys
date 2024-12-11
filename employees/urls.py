from django.urls import path
from . import views

urlpatterns = [
    path('create-employee/', views.CreateEmployeeAPIView.as_view(), name='create-employee'),
    path('find-employee/<int:user_id>/', views.RetrieveEmployeeAPIView.as_view(), name='retrieve-employee'),
    path('update-employee/<int:user_id>/', views.UpdateEmployeeAPIView.as_view(), name='update-employee'),
    path('delete-employee/<int:user_id>/', views.DeleteEmployeeAPIView.as_view(), name='delete-employee'),
    path('view-all-employees/', views.ListEmployeeAPIView.as_view(), name='list-employees'),
    path('view-profile/', views.EmployeeProfileAPIView.as_view(), name='view-employee-profile'),
]