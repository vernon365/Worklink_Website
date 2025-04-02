# job_postings/views.py
from accounts.models import CustomUser
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import JobPosting, SavedJob
from profiles.models import EmployerProfile
from datetime import datetime
from notifications.models import EmployerNotification, JobPostingNotification
from applications.models import Application
from django.utils import timezone


def test(request):
    print("Test Work")



@login_required
def create_job_posting(request):
    
    JOB_TYPE_CHOICES = JobPosting.JOB_TYPE_CHOICES  # Reference your model choices
    EXPERIENCE_LEVEL_CHOICES = JobPosting.EXPERIENCE_LEVEL_CHOICES
    PROVINCE_CHOICES = JobPosting.PROVINCE_CHOICES
    INDUSTRY_CHOICES = JobPosting.INDUSTRY_CHOICES
    
    if not hasattr(request.user, 'employer_profile'):
        return redirect('home')  # Redirect if the user is not an employer

    if request.method == 'POST':
        # Job Details
        title = request.POST.get('title')
        description = request.POST.get('description')
        job_type = request.POST.get('job_type')
        location = request.POST.get('location')
        industry = request.POST.get('industry')  # Get the industry from the form
        salary_range = request.POST.get('salary_range')
        application_deadline_str = request.POST.get('application_deadline')  # Get the datetime-local string

        # Convert the application_deadline to a Python datetime object
        if application_deadline_str:
            application_deadline = datetime.strptime(application_deadline_str, '%Y-%m-%dT%H:%M')
        else:
            application_deadline = None  # Handle case where no deadline is provided

        # Requirements
        experience_level = request.POST.get('experience_level')
        required_skills = request.POST.get('required_skills')
        education_required = request.POST.get('education_required')

        # Application Details
        contact_email = request.POST.get('contact_email')
        is_active = request.POST.get('is_active', False)  # Checkbox value

        employer = request.user
        company = employer.employer_profile.company  # Assuming the employer has a profile linking to a company

        # Create the JobPosting object
        job = JobPosting.objects.create(
            employer=employer,
            company=company,  # Assign the company
            title=title,
            description=description,
            job_type=job_type,
            location=location,
            industry=industry,  # Include the industry
            salary_range=salary_range,
            application_deadline=application_deadline,
            experience_level=experience_level,
            required_skills=required_skills,
            education_required=education_required,
            contact_email=contact_email,
            is_active=True if is_active == 'on' else False,
        )

        jobseekers = CustomUser.objects.filter(role='job_seeker')
        for js in jobseekers:
            JobPostingNotification.objects.create(
                job = job,
                jobseeker = js.job_seeker_profile,
                message = f"New Job: {job.title}",
                timestamp = timezone.now(),
                is_read = False
            )
        
        return redirect('home')

        
    context = {
        'JOB_TYPE_CHOICES': JOB_TYPE_CHOICES,
        'EXPERIENCE_LEVEL_CHOICES': EXPERIENCE_LEVEL_CHOICES,
        'PROVINCE_CHOICES': PROVINCE_CHOICES,
        'INDUSTRY_CHOICES': INDUSTRY_CHOICES,
    }
        

    return render(request, 'jobpostings/create_job_posting.html', context)




@login_required
def edit_job_posting(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id)

    if request.method == 'POST':
        job_posting.title = request.POST.get('title', job_posting.title)
        job_posting.description = request.POST.get('description', job_posting.description)
        job_posting.job_type = request.POST.get('job_type', job_posting.job_type)
        job_posting.location = request.POST.get('location', job_posting.location)
        job_posting.remote = request.POST.get('remote') == 'on'
        job_posting.salary_range = request.POST.get('salary_range', job_posting.salary_range)

        # Convert posted_date from string to datetime
        posted_date_str = request.POST.get('posted_date')
        if posted_date_str:
            job_posting.posted_date = datetime.strptime(posted_date_str, '%Y-%m-%dT%H:%M')

        # Convert application_deadline from string to datetime
        application_deadline_str = request.POST.get('application_deadline')
        if application_deadline_str:
            job_posting.application_deadline = datetime.strptime(application_deadline_str, '%Y-%m-%dT%H:%M')

        job_posting.experience_level = request.POST.get('experience_level', job_posting.experience_level)
        job_posting.required_skills = request.POST.get('required_skills', job_posting.required_skills)
        job_posting.education_required = request.POST.get('education_required', job_posting.education_required)
        job_posting.contact_email = request.POST.get('contact_email', job_posting.contact_email)
        job_posting.is_active = request.POST.get('is_active') == 'on'
        
        job_posting.save()
        return redirect('home')

    return render(request, 'jobpostings/edit_job_posting.html', {'job_posting': job_posting})


def list_job_postings(request):
    job_postings = JobPosting.objects.all()
    return render(request, 'jobpostings/job_postings.html', {'job_postings': job_postings})


def view_detail_job_posting(request, job_id):
    
    referer = request.META.get('HTTP_REFERER')
    job = JobPosting.objects.get(pk=job_id)
    saved_jobs = SavedJob.objects.filter(jobseeker=request.user)
    saved = False
    applied = False
    applications = Application.objects.filter(job_seeker=request.user)
    
    try:
        app = Application.objects.get(job_posting=job, job_seeker=request.user)
    except Application.DoesNotExist:
        app = None  # or handle the absence of the application as needed
        print(f"No application found for user {request.user} for job {job.title}.")
    except Exception as e:
        app = None  # Handle any other exceptions
        print(f"Error fetching application for user {request.user} for job {job.title}: {e}")

    
    
    for sj in saved_jobs:
        if sj.job == job:
            saved = True
            break
    
    for app in applications:
        if app.job_posting == job:
            applied = True
            break
        
            
    context = {
        'job' : job,
        'saved' : saved,
        'applied' : applied,
        'app' : app,
        'referer' : referer
    }
    return render(request, 'jobpostings/detail_jobposting.html', context)

@login_required
def delete_job_posting(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id, employer=request.user.employer_profile)

    if request.method == 'POST':
        job_posting.delete()
        return redirect('list_job_postings')

    return render(request, 'job_postings/confirm_delete_job_posting.html', {'job_posting': job_posting})

# @login_required
# def delete_job_posting(request, job_id):
#     job_posting = get_object_or_404(JobPosting, id=job_id, employer=request.user.employer_profile)

#     if request.method == 'POST':
#         job_posting.delete()
#         return redirect('list_job_postings')

#     return render(request, 'job_postings/confirm_delete_job_posting.html', {'job_posting': job_posting})


@login_required
def save_job(request, job_id):
    job = get_object_or_404(JobPosting, pk=job_id)

    
    saved_job = SavedJob.objects.create(
        jobseeker = request.user,
        job = job
    )
    
    return redirect('view_detail_job_posting', job.id)

    
def employer_view_job(request, job_id):
    job = JobPosting.objects.get(id=job_id)
    context = {
        'job' : job
    }
    return render(request, 'jobpostings/employer_job_view.html', context)











from django.http import JsonResponse
from .models import JobPosting



def fetch_jobs(request):
    print("Fetching jobs based on filters...")

    job_type = request.GET.get('job_type', '').strip()
    region = request.GET.get('region', '').strip()
    industry = request.GET.get('industry', '').strip()

    # Start with all active jobs
    jobs = JobPosting.objects.filter(is_active=False)

    # Apply filters based on user input
    if job_type:
        jobs = jobs.filter(job_type__icontains=job_type)
    if region:
        jobs = jobs.filter(location__icontains=region)
    if industry:
        jobs = jobs.filter(industry__icontains=industry)

    # Check if any jobs were found
    if not jobs.exists():
        return JsonResponse({"jobs": [], "message": "No jobs found."}, status=200)

    # Convert jobs to a list of dictionaries, ensuring proper field access
    job_list = []
    for job in jobs:
        employer_name = job.employer.employer_profile.first_name
        job_info = {
            'id' : job.id,
            'title': job.title,
            'employer_name': employer_name,
            'description': job.description,
            'job_type': job.job_type,
            'application_deadline': job.application_deadline,
            'posted_date': job.posted_date,
            'required_skills': job.required_skills,
            'education_required': job.education_required,
            'contact_email': job.contact_email,
        }
        
        # Add company information, handling if company or logo is None
        if job.company:
            job_info['company_name'] = job.company.name
            job_info['company_logo'] = job.company.logo.url if job.company.logo else None
        else:
            job_info['company_name'] = None
            job_info['company_logo'] = None

        job_list.append(job_info)

    return JsonResponse({"jobs": job_list, "message": "Jobs fetched successfully."}, status=200)
