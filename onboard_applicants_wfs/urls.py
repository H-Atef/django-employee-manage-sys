from django.urls import path
from . import views

urlpatterns = [
    path('view-applicants/', views.OnBoardingApplicantListView.as_view(), name='applicant-list'),
    path('search-applicant/<int:pk>/', views.OnBoardingApplicantDetailView.as_view(), name='applicant-detail'),
    path('create-applicant/', views.OnBoardingApplicantCreateView.as_view(), name='applicant-create'),
    path('update-applicant/<int:pk>/', views.OnBoardingApplicantUpdateStageView.as_view(), name='applicant-update-stage'),
    path('delete-rejected-applicants/', views.OnBoardingApplicantDeleteRejectedView.as_view(), name='applicant-delete-rejected'),
]
