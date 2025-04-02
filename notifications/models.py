# notifications/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from profiles.models import JobSeekerProfile
from jobpostings.models import JobPosting
from teams.models import Team

User = get_user_model()

class JobPostingNotification(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='job_posting_notifications')
    jobseeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, null=True, related_name="job_seeker_notifications_job")
    message = models.TextField()  # The notification message, e.g., "New job posted"
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)  # Track if the notification is read

    def __str__(self):
        return f"New Job: {self.job}"

    class Meta:
        ordering = ['-timestamp']  # Sort by most recent notifications first
        
        
class EmployerNotification(models.Model):
    applicant = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='employer_notifications')
    employer = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField()
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, null=True, related_name='employer_job_notifications')
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for  - {self.message}"

class TeamJoinRequestNotification(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, related_name='my_team_requests_notifications')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, related_name='team_request_notifications')
    message = models.TextField(null=True)
    is_read = models.BooleanField(default=False)
    is_for_admin = models.BooleanField(default=True)  # New field to indicate it's for the admin
    is_for_requester = models.BooleanField(default=False)  # New field to indicate it's for the requester
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.message


    
    