from rest_framework import serializers
from .models import EmployerNotification, JobPostingNotification

class JobPostingNotificationSerializer(serializers.ModelSerializer):
    # Represent the related JobPosting and applicant with StringRelatedField or PrimaryKeyRelatedField
    job = serializers.StringRelatedField()  # Or use PrimaryKeyRelatedField() if you want just the job ID
    applicant = serializers.StringRelatedField()  # Or use PrimaryKeyRelatedField() if you want just the applicant ID

    class Meta:
        model = JobPostingNotification  # The updated model
        fields = ['id', 'job', 'applicant', 'message', 'timestamp', 'is_read']  
        
        
class EmployerNotificationSerializer(serializers.ModelSerializer):
    applicant = serializers.StringRelatedField()  # or serializers.PrimaryKeyRelatedField() if you want just IDs
    employer = serializers.StringRelatedField()  # or serializers.PrimaryKeyRelatedField() if you want just IDs
    job = serializers.StringRelatedField()  # or serializers.PrimaryKeyRelatedField() if you want just IDs

    class Meta:
        model = EmployerNotification
        fields = ['id', 'applicant', 'employer', 'message', 'job', 'timestamp', 'is_read']
