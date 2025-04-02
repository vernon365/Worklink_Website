
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Application
from .models import JobPostingApplication
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from jobpostings.models import JobPosting, Interview, SavedJob
from notifications.models import EmployerNotification
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST


@login_required
def list_applications(request):
    applications = Application.objects.filter(job_seeker=request.user)
    return render(request, 'applications/list_applications.html', {'applications': applications})


@login_required
def view_application(request, app_id):
    application = get_object_or_404(Application, id=app_id)
    
    return render(request, 'applications/view_application.html', {'application': application})


@login_required
def apply_to_job(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id)

    if request.method == 'POST':
        cover_letter = request.FILES['cover_letter']
        resume = request.FILES['resume']

        application = Application.objects.create(
            job_posting=job_posting,
            job_seeker=request.user,
            cover_letter=cover_letter,
            resume=resume
        )

        # Create a notification for the employer
        employer_user = job_posting.employer
        message = f"New application for {job_posting.title} from {request.user.username}."
        
        
        notification_msg = f"{request.user.job_seeker_profile.first_name} has applied to the job you posted: {job_posting}"
        notification = EmployerNotification.objects.create(
            employer = job_posting.employer,
            message = notification_msg,
            applicant = request.user,
            job = job_posting
        )
        
        print(notification)
        
        job_app = JobPostingApplication.objects.create(job_posting=job_posting, applicant=request.user)

        return redirect('job_seeker_db')

    return render(request, 'applications/job_application.html', {'job_posting': job_posting})


@login_required
def manage_applications(request, job_id):
    job_posting = get_object_or_404(JobPosting, id=job_id, employer=request.user)
    applications = Application.objects.filter(job_posting=job_posting)

    return render(request, 'applications/manage_applications.html', {'job_posting': job_posting, 'applications': applications})

@login_required
def update_application_status(request, application_id, status):
    application = get_object_or_404(Application, id=application_id)

    if request.user != application.job_posting.employer:
        messages.error(request, "You are not authorized to change the status of this application.")
        return redirect('list_job_postings')

    application.status = status
    application.save()

    # Create a notification for the job seeker
    message = f"Your application for {application.job_posting.title} has been {status}."
    # Notification.objects.create(user=application.job_seeker, message=message)


    return redirect('manage_applications', job_id=application.job_posting.id)


# applications/views.py

@login_required
def accept_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, job_posting__employer=request.user)

    if request.method == 'POST':
        application.status = 'accepted'
        application.save()

        # Notify the job seeker
        # Notification.objects.create(
        #     user=application.job_seeker,
        #     message=f"Your application for job '{application.job_posting.title}' has been accepted."
        # )

        return redirect('home')

    return render(request, 'applications/confirm_accept_application.html', {'application': application})


@login_required
def reject_application(request, application_id):
    application = get_object_or_404(Application, id=application_id, job_posting__employer=request.user)

    if request.method == 'POST':
        application.status = 'rejected'
        application.save()

        # Notify the job seeker
        # Notification.objects.create(
        #     user=application.job_seeker,
        #     message=f"Your application for job '{application.job_posting.title}' has been rejected."
        # )

        return redirect('home')

    return render(request, 'applications/confirm_reject_application.html', {'application': application})


def application_succeed(request):
    return render(request, 'applications/apply_success.html')



def my_applications(request, id):
    Users = get_user_model()
    user = Users.objects.get(id=id)
    applications = user.applications.all()
    context = {
        'my_applications' : applications
    }
    
    return render(request, 'applications/my_applications.html',context)


def applications(request):
    applications = Application.objects.all()
    context = {
        'applications' : applications
    }
    return render(request, 'applications/manage_applications.html', context)


def confirm_application(request, id):
    application_id = id
    if request.method == 'POST':
        application = get_object_or_404(Application, id=id)
        application.status = 'accepted'
        application.save()

        print(f"----------------------------------------------{application.status}")
        return redirect('home')
    return render(request, 'applications/application_confirm.html')


def reject_application(request, id):
    if request.method == 'POST':
        application = get_object_or_404(Application, id=id)
        application.status = 'rejected'
    return render(request, 'applications/reject_application.html')




@csrf_exempt
def update_application_status(request):
    if request.method == 'POST':
        is_accepted = False
        # Get data from the request body
        data = json.loads(request.body)
        application_id = data.get('application_id')
        print("application id")
        print(application_id)
        status = data.get('status')

        # Check if the status is valid
        if status not in dict(Application.STATUS_CHOICES).keys():
            return JsonResponse({'status': 'error', 'message': 'Invalid status'}, status=400)

        try:
            # Fetch the application and update the status
            application = Application.objects.get(id=application_id)
            application.status = status
            is_accepted = True
            application.save()
            

            return JsonResponse({'status': 'success', 'message': 'Application status updated'})
        except Application.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Application not found'}, status=404)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
    
    
def view_job_seeker_db(request):
    user = request.user
    applications = Application.objects.filter(job_seeker=user)
    saved_jobs = SavedJob.objects.filter(jobseeker=user)
    
    print(f"saved jobs {saved_jobs.count()}")
    print(f"user applications {applications.count()}")
    
    context = {
        'applications' : applications,
        'saved_jobs' : saved_jobs   
    }
    
    return render(request, 'applications/job_seeker_dashboard.html', context)









def delete_application(request, application_id):
    # Get the application to be deleted
    application = get_object_or_404(Application, id=application_id)
    print("----------------------------------adfsdfs------------")
    # Ensure the request comes from the job seeker who applied
    if request.user == application.job_seeker:
        application.delete()
        return redirect('job_seeker_db')
    else:
        return JsonResponse({'success': False, 'error': 'Unauthorized'}, status=403)
    
    
    
    
    
def request_application_delete(request, id):
    application = get_object_or_404(Application, id=id)
    
    context = {
        'application' : application,
    }
    
    return render(request, 'applications/delete_application.html', context)



def view_my_application(request, id):
    referer = request.META.get('HTTP_REFERER')
    application = get_object_or_404(Application, id=id)
    
    context = {
        'application' : application,
        'referer' : referer
    }
    
    return render(request, 'applications/view_my_application.html', context)



