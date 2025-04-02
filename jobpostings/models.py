from django.db import models
from django.contrib.auth import get_user_model
from profiles.models import Company, EmployerProfile
from datetime import datetime, timedelta
from django.utils import timezone
from accounts.models import CustomUser


class JobPosting(models.Model):
    PROVINCE_CHOICES = [
        ('central', 'Central'),
        ('gulf', 'Gulf'),
        ('oro', 'Oro'),
        ('southern-highlands', 'Southern Highlands'),
        ('hela', 'Hela'),
        ('western-highlands', 'Western Highlands'),
        ('enga', 'Enga'),
        ('east-sepik', 'East Sepik'),
        ('west-sepik', 'West Sepik (Sandaun)'),
        ('madang', 'Madang'),
        ('morobe', 'Morobe'),
        ('new-ireland', 'New Ireland'),
        ('east-new-britain', 'East New Britain'),
        ('west-new-britain', 'West New Britain'),
        ('bougainville', 'Bougainville'),
        ('milne-bay', 'Milne Bay'),
        ('northern', 'Northern'),
        ('chimbu', 'Chimbu (Simbu)'),
        ('jiwaka', 'Jiwaka'),
        ('western', 'Western'),
        ('national-capital-district', 'National Capital District'),
    ]

    INDUSTRY_CHOICES = [
        ('healthcare', 'Healthcare - Hospitals, Clinics, Pharmaceuticals'),
        ('information-technology', 'Information Technology - Software, IT Services, Cybersecurity'),
        ('finance', 'Finance - Banking, Investment, Insurance'),
        ('education', 'Education - Schools, Universities, Online Learning'),
        ('manufacturing', 'Manufacturing - Automotive, Electronics, Food Production'),
        ('construction', 'Construction - Residential, Commercial, Infrastructure'),
        ('retail', 'Retail - E-commerce, Fashion, Grocery Stores'),
        ('hospitality', 'Hospitality - Hotels, Restaurants, Tourism'),
        ('marketing-and-advertising', 'Marketing and Advertising - PR, Digital Marketing, Branding'),
        ('telecommunications', 'Telecommunications - Network Services, Mobile, Satellite'),
        ('transportation-and-logistics', 'Transportation and Logistics - Shipping, Supply Chain, Public Transit'),
        ('energy-and-utilities', 'Energy and Utilities - Oil and Gas, Renewable Energy, Water Supply'),
        ('real-estate', 'Real Estate - Residential Sales, Commercial Leasing, Property Management'),
        ('government-and-public-administration', 'Government and Public Administration - Local, Federal, Military'),
        ('legal-services', 'Legal Services - Law Firms, Compliance, Corporate Counsel'),
        ('media-and-entertainment', 'Media and Entertainment - Film, TV, Publishing, Gaming'),
        ('agriculture', 'Agriculture - Farming, Animal Husbandry, Food Processing'),
        ('non-profit-and-ngos', 'Non-Profit and NGOs - Charity, Advocacy, International Development'),
        ('science-and-research', 'Science and Research - Academic, Clinical Trials, Private Labs'),
        ('human-resources', 'Human Resources - Recruitment, Employee Relations, Training'),
    ]

    JOB_TYPE_CHOICES = [
        ('FT', 'Full-time'),
        ('PT', 'Part-time'),
        ('CT', 'Contract'),
        ('FL', 'Freelance'),
        ('IN', 'Internship'),
        ('FJ', 'Fast Job'),
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ('Entry', 'Entry Level'),
        ('Mid', 'Mid Level'),
        ('Senior', 'Senior Level'),
    ]

    # Add the fields using these choices
    location = models.CharField(max_length=50, choices=PROVINCE_CHOICES)
    industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES, null=True)
    job_type = models.CharField(max_length=2, choices=JOB_TYPE_CHOICES)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_LEVEL_CHOICES)

    # Rest of your fields
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateTimeField(blank=True, null=True)
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_postings')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, related_name='job_postings')
    required_skills = models.TextField(help_text="List the required skills, separated by commas.")
    education_required = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField()
    is_active = models.BooleanField(default=True)

    
    class Meta:
        ordering = ['-posted_date'] 

    def __str__(self):
        return self.title

    @classmethod
    def posted_today(cls):
        today_start = timezone.now().date()
        today_end = today_start + timedelta(days=1)
        return cls.objects.filter(posted_date__date__gte=today_start, posted_date__date__lt=today_end)

    @classmethod
    def posted_this_week(cls):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return cls.objects.filter(posted_date__date__range=(start_of_week, end_of_week))

    @classmethod
    def posted_this_month(cls):
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        next_month = start_of_month.replace(month=today.month % 12 + 1)
        end_of_month = next_month - timedelta(days=1)
        return cls.objects.filter(posted_date__date__range=(start_of_month, end_of_month))

    @classmethod
    def get_total_applications_for_user(cls, user):
        # Get all job postings by the user
        from applications.models import Application 
        job_postings = cls.objects.filter(employer=user)

        # Count the total number of applications for these job postings
        total_applications = Application.objects.filter(job_posting__in=job_postings).count()

        return total_applications
    
    def get_total_applications(self):
        # Count the number of applications for this job posting
        return self.applications.count()
    
    def get_applications(self):
        # Count the number of applications for this job posting
        return self.applications.all()



class SavedJob(models.Model):
    jobseeker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='saved_jobs')
    
    def __str__(self):
        return f"{self.jobseeker} - {self.job.title}"


class Interview(models.Model):
    job_seeker = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='interview')
    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='job_seeker_interview')
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=50, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')])

    def __str__(self):
        return f'Interview for {self.job_seeker} with {self.employer} on {self.date}'
    
    
