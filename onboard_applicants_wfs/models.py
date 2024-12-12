from django.db import models


class OnboardingStage(models.TextChoices):
    APPLICATION_RECEIVED = 'Application Received'
    INTERVIEW_SCHEDULED = 'Interview Scheduled'
    HIRED = 'Hired'
    NOT_ACCEPTED = 'Not Accepted'



class OnBoardingApplicant(models.Model):
    applicant_name = models.CharField(max_length=255)
    stage=models.CharField(max_length=20,
                           choices=OnboardingStage.choices,default=OnboardingStage.APPLICATION_RECEIVED)
    
    class Meta:
        verbose_name = "Onboarding Applicant"
        verbose_name_plural = "Onboarding Applicants"
        ordering = ['-id']  # Order applicants by id descending (most recent first)

    def __str__(self):
        return f"{self.applicant_name} - {self.stage}"