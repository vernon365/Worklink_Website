from django.shortcuts import render
from jobpostings.models import JobPosting
from applications.models import Application
from profiles.models import Company, JobSeekerProfile
from teams.models import Team, TeamJobseeker, TeamJoinRequest
from collections import Counter
from django.db.models import Count
from django.db.models import Count
from django.shortcuts import render


from django.db.models import Count

def get_industry_profile_data():
    """
    Fetches industry profile data with profile counts and details of associated job seekers.

    Returns:
        dict: A dictionary with industry names as keys. Each key maps to a dictionary containing:
            - 'profile_count': (int) Number of profiles in the industry.
            - 'profiles': (list) A list of dictionaries with details ('id', 'first_name', 'last_name', 'profile_photo') of job seekers.
    """
    # Fetch industries and their profile counts
    industry_profile_counts = (
        JobSeekerProfile.objects.values('industry')
        .annotate(profile_count=Count('id'))
    )

    # Build the dictionary with profile data for each industry
    industry_profile_data = {}
    for item in industry_profile_counts:
        industry = item['industry']
        profiles = list(
            JobSeekerProfile.objects.filter(industry=industry)
            .values('id', 'first_name', 'last_name', 'profile_photo')
        )
        # Append the full URL for the profile photo
        for profile in profiles:
            profile['profile_photo'] = profile['profile_photo'] or ''  # Handle cases where photo is not set
            if profile['profile_photo']:
                profile['profile_photo'] = JobSeekerProfile.profile_photo.field.storage.url(profile['profile_photo'])

        industry_profile_data[industry] = {
            'profile_count': item['profile_count'],
            'profiles': profiles,
        }

    return industry_profile_data



def get_school_profile_data():
    """
    Fetches school or university profile data with profile counts and details of associated job seekers.

    Returns:
        dict: A dictionary with school/university names as keys. Each key maps to a dictionary containing:
            - 'profile_count': (int) Number of profiles from the school/university.
            - 'profiles': (list) A list of dictionaries with details ('id', 'first_name', 'last_name', 'profile_photo') of job seekers.
    """
    # Fetch schools/universities and their profile counts
    school_profile_counts = (
        JobSeekerProfile.objects.values('school_or_university')
        .annotate(profile_count=Count('id'))
    )

    # Build the dictionary with profile data for each school/university
    school_profile_data = {}
    for item in school_profile_counts:
        school = item['school_or_university']
        profiles = list(
            JobSeekerProfile.objects.filter(school_or_university=school)
            .values('id', 'first_name', 'last_name', 'profile_photo')
        )
        # Append the full URL for the profile photo
        for profile in profiles:
            profile['profile_photo'] = profile['profile_photo'] or ''  # Handle cases where photo is not set
            if profile['profile_photo']:
                profile['profile_photo'] = JobSeekerProfile.profile_photo.field.storage.url(profile['profile_photo'])

        school_profile_data[school] = {
            'profile_count': item['profile_count'],
            'profiles': profiles,
        }

    return school_profile_data



def get_contact_page(request):
    return render(request, 'general/contact.html')


def get_about_page(request):
    return render(request, 'general/about.html')


def get_trending_industries():
    jobpostings = JobPosting.objects.all()
    
    industry_counter = Counter(job.industry for job in jobpostings)
    industry_jobs_list = [
        {"industry": industry, "jobs": count} 
        for industry, count in industry_counter.items()
    ]
    
    industry_jobs_list.sort(key=lambda x: x["jobs"], reverse=True)
    return industry_jobs_list


def home(request):
    user = request.user
    JOB_TYPE_CHOICES = JobPosting.JOB_TYPE_CHOICES 
    EXPERIENCE_LEVEL_CHOICES = JobPosting.EXPERIENCE_LEVEL_CHOICES
    PROVINCE_CHOICES = JobPosting.PROVINCE_CHOICES
    INDUSTRY_CHOICES = JobPosting.INDUSTRY_CHOICES

    # Fetch industry and school data
    industry_profile_data = get_industry_profile_data()
    school_profile_data = get_school_profile_data()


    jobpostings = JobPosting.objects.all()
    applications = Application.objects.all()
    companies = Company.objects.all()
    teams = Team.objects.all()
    team_request = TeamJoinRequest.objects.all()
    job_seeker_profiles = JobSeekerProfile.objects.all()


    total_jobs = jobpostings.count()
    top_three_companies_list = []
    for c in companies:
        top_three_companies_list.append((c, c.job_postings.count()))
    top_three_companies_list.sort(key=lambda x: x[1], reverse=True)
    top_three_companies = [company for company, _ in top_three_companies_list[:3]]
    jobs = []
    my_applications = Application.objects.filter(job_seeker=user) if user.is_authenticated else []

    for job in jobpostings:
        applied = False
        this_job_app = None    
        try:
            employer_profile = getattr(job.employer, 'employer_profile', None)
            individual_profile = getattr(job.employer, 'individual_employer_profile', None)


            if employer_profile and employer_profile.company:
                profile_type = 'EmployerProfile'
                company_name = employer_profile.company.name
                company_logo = employer_profile.company.logo.url if employer_profile.company.logo else None
                profile_name = None  # No need for individual name if associated with a company

            # For individual employers, display their name and profile photo
            elif individual_profile:
                profile_type = 'IndividualEmployerProfile'
                profile_name = f"{individual_profile.first_name} {individual_profile.last_name}"
                company_name = None  # No company name for individual employers
                company_logo = individual_profile.profile_photo.url if individual_profile.profile_photo else None

            # Fallback if no profile information is available
            else:
                profile_type = None
                company_name = None
                profile_name = None
                company_logo = None

            # Check if the user has applied for the job
            for myapp in my_applications:
                if myapp.job_posting == job:
                    applied = True
                    this_job_app = myapp
                    print(f"{user} has already applied for the {job}")
                    print(f"here is the app {myapp}")
                    break

            # Building job information for the frontend display
            job_info = {
                'id': job.id,
                'title': job.title,
                'employer': job.employer,
                'description': job.description,
                'applied': applied,
                'app' : this_job_app,
                'employer_profile_type': profile_type,
                'employer_company_name': company_name,
                'employer_profile_name': profile_name,
                'employer_company_logo': company_logo,
                'job_type': job.get_job_type_display(),
                'location': job.location,
                'salary_range': job.salary_range,
                'posted_date': job.posted_date,
                'application_deadline': job.application_deadline,
                'experience_level': job.get_experience_level_display(),
                'required_skills': job.required_skills,
                'education_required': job.education_required,
                'contact_email': job.contact_email,
                'is_active': job.is_active,
                'application_count': job.get_applications().count(),
                'applications': job.get_applications(),  # List of job applications
            }

            jobs.append(job_info)
        except Exception as e:
            print(f"Error processing job {job.id}: {e}")
            
    trending_industries = get_trending_industries()
    
    context = {
        'jobpostings': jobs,
        'applications': applications,
        'top_companies': top_three_companies,
        'teams': teams,
        'requests': team_request,
        'JOB_TYPE_CHOICES': JOB_TYPE_CHOICES,
        'EXPERIENCE_LEVEL_CHOICES': EXPERIENCE_LEVEL_CHOICES,
        'PROVINCE_CHOICES': PROVINCE_CHOICES,
        'INDUSTRY_CHOICES': INDUSTRY_CHOICES,
        'total_jobs': total_jobs,  # Add total job count here
        'industries' : trending_industries,
        'job_seeker_profiles' : job_seeker_profiles,
        'industry_profile_data': industry_profile_data,  # Add this line
        'school_profile_data' : school_profile_data
    }
    

    return render(request, 'home.html', context)



