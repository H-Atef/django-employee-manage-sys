from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from onboard_applicants_wfs.models import OnBoardingApplicant, OnboardingStage
from onboard_applicants_wfs.serializers import OnBoardingApplicantSerializer
from rest_framework.permissions import IsAuthenticated
from onboard_applicants_wfs.permissions.role_permission import IsManagerOrAdmin
from users.security.custom_jwt_auth import CustomJWTAuthentication

# 1. Retrieve All Onboarding Applicants
class OnBoardingApplicantListView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    authentication_classes = [CustomJWTAuthentication]


    def get(self, request):
        """
        Retrieve all onboarding applicants.
        """
        applicants = OnBoardingApplicant.objects.all()
        serializer = OnBoardingApplicantSerializer(applicants, many=True)
        return Response(serializer.data)


# 2. Retrieve One Onboarding Applicant
class OnBoardingApplicantDetailView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    authentication_classes = [CustomJWTAuthentication]


    def get(self, request, pk):
        """
        Retrieve a single onboarding applicant by ID.
        """
        try:
            applicant = OnBoardingApplicant.objects.get(id=pk)
        except OnBoardingApplicant.DoesNotExist:
            return Response({"detail": "Applicant not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OnBoardingApplicantSerializer(applicant)
        return Response(serializer.data)


# 3. Create New Onboarding Applicant
class OnBoardingApplicantCreateView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    authentication_classes = [CustomJWTAuthentication]


    def post(self, request):
        """
        Create a new onboarding applicant.
        """
        serializer = OnBoardingApplicantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 4. Update Onboarding Applicant Stage
class OnBoardingApplicantUpdateStageView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    authentication_classes = [CustomJWTAuthentication]


    def patch(self, request, pk):
        """
        Update the onboarding applicant's stage.
        """
        try:
            applicant = OnBoardingApplicant.objects.get(id=pk)
        except OnBoardingApplicant.DoesNotExist:
            return Response({"detail": "Applicant not found."}, status=status.HTTP_404_NOT_FOUND)

        new_stage = request.data.get('stage')
        if not new_stage:
            return Response({"detail": "New stage is required."}, status=status.HTTP_400_BAD_REQUEST)

        if new_stage not in dict(OnboardingStage.choices):
            return Response({"detail": "Invalid stage."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if transition is valid
        valid_transitions = {
            OnboardingStage.APPLICATION_RECEIVED: [OnboardingStage.INTERVIEW_SCHEDULED, OnboardingStage.NOT_ACCEPTED],
            OnboardingStage.INTERVIEW_SCHEDULED: [OnboardingStage.HIRED, OnboardingStage.NOT_ACCEPTED],
        }

        current_stage = applicant.stage
        if new_stage not in valid_transitions.get(current_stage, []):
            return Response({"detail": "Invalid stage transition."}, status=status.HTTP_400_BAD_REQUEST)

        applicant.stage = new_stage
        applicant.save()

        serializer = OnBoardingApplicantSerializer(applicant)
        return Response(serializer.data, status=status.HTTP_200_OK)


# 5. Delete Rejected Applicants (Not Accepted)
class OnBoardingApplicantDeleteRejectedView(APIView):
    permission_classes = [IsAuthenticated, IsManagerOrAdmin]
    authentication_classes = [CustomJWTAuthentication]


    def delete(self, request):
        """
        Delete all applicants who have been rejected (Not Accepted).
        """
        applicants = OnBoardingApplicant.objects.filter(stage=OnboardingStage.NOT_ACCEPTED)
        deleted_count = applicants.count()
        if deleted_count > 0:
            applicants.delete()
            return Response({"detail": f"{deleted_count} applicants deleted."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "No rejected applicants found."}, status=status.HTTP_404_NOT_FOUND)
