from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True, null=True)
    
    def __str__(self):
        return self.email if self.email else self.username  # Fallback to username if email is None
    