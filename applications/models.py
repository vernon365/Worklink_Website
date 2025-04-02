# applications/models.py

from django.db import models
from jobpostings.models import JobPosting  # Import the JobPosting model from the job_postings app
from django.contrib.auth import get_user_model

User = get_user_model()

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    job_seeker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.FileField(upload_to='cover_letters/')
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    applicant_profile = models.ForeignKey('profiles.JobSeekerProfile', on_delete=models.CASCADE, null=True, related_name='applications')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.job_seeker.username} - {self.job_posting.title}"
    

class JobPostingApplication(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='job_posting_ja')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications_ja')
    
    def __str__(self):
        return f"{self.job_posting} - {self.applicant}"
    

