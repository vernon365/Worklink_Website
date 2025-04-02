from django.db import models
from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.conf import settings




class JobSeekerProfile(models.Model):
    PROVINCE_CHOICES = [
        ('NCD', 'National Capital District'),
        ('Central', 'Central Province'),
        ('Milne Bay', 'Milne Bay Province'),
        ('Oro', 'Oro Province'),
        ('Western', 'Western Province'),
        ('Gulf', 'Gulf Province'),
        ('Morobe', 'Morobe Province'),
        ('Madang', 'Madang Province'),
        ('East Sepik', 'East Sepik Province'),
        ('West Sepik', 'West Sepik (Sandaun) Province'),
        ('Enga', 'Enga Province'),
        ('Southern Highlands', 'Southern Highlands Province'),
        ('Hela', 'Hela Province'),
        ('Western Highlands', 'Western Highlands Province'),
        ('Jiwaka', 'Jiwaka Province'),
        ('Eastern Highlands', 'Eastern Highlands Province'),
        ('Simbu', 'Simbu Province'),
        ('Bougainville', 'Autonomous Region of Bougainville'),
        ('East New Britain', 'East New Britain Province'),
        ('West New Britain', 'West New Britain Province'),
        ('New Ireland', 'New Ireland Province'),
        ('Manus', 'Manus Province'),
    ]


    SCHOOL_CHOICES = [
        ('UPNG', 'University of Papua New Guinea (UPNG)'),
        ('UNITECH', 'Papua New Guinea University of Technology (UNITECH)'),
        ('UOG', 'University of Goroka (UOG)'),
        ('UNRE', 'University of Natural Resources and Environment (UNRE)'),
        ('WPU', 'Western Pacific University (WPU)'),
        ('DWU', 'Divine Word University (DWU)'),
        ('PAU', 'Pacific Adventist University (PAU)'),
        ('IBS', 'Institute of Business Studies (IBS) University'),
        ('LTI', 'Legal Training Institute (LTI)'),
        ('PNGMC', 'PNG Maritime College'),
        ('MAPEX', 'Mapex Training Institute'),
        ('MadangTC', 'Madang Teachers\' College'),
        ('HolyTrinityTC', 'Holy Trinity Teachers\' College'),
        ('StBenedictsTC', 'St. Benedict’s Teachers\' College'),
        ('BalobTC', 'Balob Teachers\' College'),
        ('LaeSN', 'Lae School of Nursing'),
        ('MadangLSN', 'Madang Lutheran School of Nursing'),
        ('StBarnabasSN', 'St. Barnabas School of Nursing'),
        ('MendiSN', 'Mendi School of Nursing'),
        ('KudjipNCN', 'Kudjip Nazarene College of Nursing'),
        ('DBTI', 'Don Bosco Technical Institute'),
        ('POMTech', 'Port Moresby Technical College'),
        ('LaeTech', 'Lae Technical College'),
        ('GorokaTech', 'Goroka Technical College'),
        ('MtHagenTech', 'Mt. Hagen Technical College'),
        ('PNGIMR', 'PNG Institute of Medical Research'),
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
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='job_seeker_profile')
    carrier = models.CharField(max_length=100, null=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    about_me = models.TextField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='job_seekers/profile_photos/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    school_or_university = models.CharField(max_length=50, choices= SCHOOL_CHOICES, blank=True, null=True)
    years_of_experience = models.IntegerField(null=True, blank=True)
    province = models.CharField(max_length=50, choices=PROVINCE_CHOICES, blank=True, null=True)
    available = models.BooleanField(default=True)
    industry = models.CharField(max_length=100, choices=INDUSTRY_CHOICES, blank=True, null=True)

    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Skill(models.Model):
    job_seeker_profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Link(models.Model):
    job_seeker_profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='links')
    name = models.CharField(max_length=50)  # e.g., "LinkedIn", "Portfolio"
    url = models.URLField()

    def __str__(self):
        return f"{self.name}: {self.url}"


class GeneralExperience(models.Model):
    job_seeker_profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=100)  # e.g., "Software Developer", "Team Lead"
    description = models.TextField()
    organization = models.CharField(max_length=100, blank=True, null=True)  # e.g., "ABC Corp", "University Project"
    referer_name = models.CharField(max_length=100, blank=True, null=True)
    referer_contact = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.title} at {self.organization or 'N/A'}"
    
    






class Company(models.Model):
    # Basic Information
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    
    admin = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)

    # Contact Information
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    # Additional Information
    size = models.CharField(max_length=100, blank=True, null=True)
    headquarters = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True, blank=True, null=True)

    # Meta Information
    
    created_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Company'
        verbose_name_plural = 'Companies'


class CompanyEmployer(models.Model):
    # Linking an employer to a company
    employer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='company_employers')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_employers')
    position = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.employer.username} - {self.company.name} ({self.position})"

    class Meta:
        unique_together = ('employer', 'company')
        verbose_name = 'Company Employer'
        verbose_name_plural = 'Company Employers'


class EmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employer_profile')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True, related_name='my_company')
    position = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='employers/profile_photos/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_admin = models.BooleanField(default=False)
    is_company_employer = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - ({self.position})"


class IndividualEmployerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='individual_employer_profile')
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(upload_to='individual/employers/profile_photos/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    is_individual_employer = models.BooleanField(default=True, blank=True, null=True)