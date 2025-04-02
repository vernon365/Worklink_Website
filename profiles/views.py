from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from profiles.models import JobSeekerProfile, EmployerProfile, Company, GeneralExperience
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from profiles.models import IndividualEmployerProfile, Skill
from django.db import IntegrityError
import logging
from django.http import JsonResponse
from accounts.models import CustomUser
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_POST


@login_required
@csrf_exempt  # Temporarily disable CSRF protection to test; remove after testing.
def add_experience(request):
    print("LLLLLLOOOOOWWW")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            profile = JobSeekerProfile.objects.get(user=request.user)

            experience = GeneralExperience.objects.create(
                job_seeker_profile=profile,
                title=data['title'],
                description=data['description'],
                organization=data.get('organization'),
                referer_name=data.get('referer_name'),
                referer_contact=data.get('referer_contact')
            )
            return JsonResponse({'success': True, 'id': experience.id})
        except JobSeekerProfile.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Profile not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=405)



def get_experiences(request):
    experiences = GeneralExperience.objects.filter(job_seeker_profile=request.user.job_seeker_profile)
    experience_data = [{
        'id': exp.id,
        'title': exp.title,
        'description': exp.description,
        'organization': exp.organization,
        'start_date': exp.start_date,
        'end_date': exp.end_date,
        'is_current': exp.is_current,
        'referer_name': exp.referer_name,
        'referer_contact': exp.referer_contact
    } for exp in experiences]
    return JsonResponse({'success': True, 'experiences': experience_data})


# Remove an experience
@csrf_exempt
@require_POST
def remove_experience(request):
    data = json.loads(request.body)
    experience_id = data.get("experience_id")

    try:
        experience = GeneralExperience.objects.get(id=experience_id)
        experience.delete()
        return JsonResponse({"success": True})
    except GeneralExperience.DoesNotExist:
        return JsonResponse({"success": False, "error": "Experience not found."}, status=404)
    
    
# Edit an existing experience
@csrf_exempt
@require_POST
def edit_experience(request):
    data = json.loads(request.body)
    experience_id = data.get("id")
    title = data.get("title")
    description = data.get("description")
    organization = data.get("organization", "")
    referer_name = data.get("referer_name", "")
    referer_contact = data.get("referer_contact", "")

    try:
        experience = GeneralExperience.objects.get(id=experience_id)
        experience.title = title
        experience.description = description
        experience.organization = organization
        experience.referer_name = referer_name
        experience.referer_contact = referer_contact
        experience.save()
        return JsonResponse({"success": True})
    except GeneralExperience.DoesNotExist:
        return JsonResponse({"success": False, "error": "Experience not found."}, status=404)


@csrf_exempt
def save_experiences(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        new_experiences = data.get('experiences', [])

        # Get the current experiences (avoid replacing them)
        current_experiences = GeneralExperience.objects.filter(job_seeker_profile=request.user.job_seeker_profile)

        # Loop through the new experiences
        for exp in new_experiences:
            # Check if this experience already exists in the database
            if not current_experiences.filter(title=exp['title'], organization=exp['organization']).exists():
                # Only add if it's not already present
                GeneralExperience.objects.create(
                    job_seeker_profile=request.user.job_seeker_profile,
                    title=exp['title'],
                    description=exp['description'],
                    organization=exp['organization'],
                    start_date=exp['start_date'],
                    end_date=exp['end_date'],
                    is_current=exp['is_current'],
                    referer_name=exp['referer_name'],
                    referer_contact=exp['referer_contact']
                )

        # Return success response
        return JsonResponse({'success': True, 'message': 'Experiences saved successfully!'})


@login_required
def get_experiences(request):
    if request.method == 'GET':
        job_seeker_profile = request.user.job_seeker_profile
        experiences = job_seeker_profile.experiences.all().values(
            'title', 'description', 'organization', 'referer_name', 'referer_contact'
        )
        return JsonResponse(list(experiences), safe=False)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


# Remove an experience
@csrf_exempt
def remove_experience(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        experience_id = data.get('experience_id')

        try:
            experience = GeneralExperience.objects.get(id=experience_id, job_seeker_profile=request.user.job_seeker_profile)
            experience.delete()
            return JsonResponse({'success': True, 'message': 'Experience deleted successfully!'})
        except GeneralExperience.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Experience not found!'})












@login_required
def get_skills(request):
    """Retrieve saved skills for the current user."""
    try:
        # Attempt to fetch the user's profile
        profile = JobSeekerProfile.objects.get(user=request.user)

        
        # Attempt to fetch skills for the user profile
        skills = Skill.objects.filter(job_seeker_profile=profile).values_list('name', flat=True)
        
        # Check if skills exist, return empty list if not
        if not skills:
            return JsonResponse({"success": True, "message": "No skills found.", "skills": []})
        
        # Return the skills if found
        return JsonResponse({"success": True, "skills": list(skills)})
    
    except JobSeekerProfile.DoesNotExist:
        # Handle case where user's profile does not exist
        return JsonResponse({"success": False, "error": "User profile not found."})
    
    except Exception as e:
        # Catch any unexpected errors
        return JsonResponse({"success": False, "error": str(e)})




@csrf_exempt
@login_required
def save_skills(request):
    print("YOOSOOSOS")
    """Save skills for the current user."""
    if request.method == "POST":
        try:
            # Attempt to fetch the user's profile
            profile = JobSeekerProfile.objects.get(user=request.user)
            print(f"Profile {profile}")
            # Parse the incoming JSON data
            data = json.loads(request.body)
            
            # Extract skills from the request data
            skills = data.get("skills", [])
            
            if not isinstance(skills, list):
                # Ensure that skills are in list format
                return JsonResponse({"success": False, "error": "Skills must be provided as a list."})
            
            if not skills:
                # Handle the case where the skills list is empty
                return JsonResponse({"success": False, "error": "No skills provided."})
            
            # Clear any existing skills for the user
            Skill.objects.filter(job_seeker_profile=profile).delete()

            # Add new skills to the profile
            for skill_name in skills:
                Skill.objects.create(job_seeker_profile=profile, name=skill_name)
            
            # Return the success response with the saved skills
            return JsonResponse({"success": True, "skills": skills})
        
        except JobSeekerProfile.DoesNotExist:
            # Handle case where user's profile does not exist
            return JsonResponse({"success": False, "error": "User profile not found."})
        
        except json.JSONDecodeError:
            # Handle invalid JSON format error
            return JsonResponse({"success": False, "error": "Invalid JSON format in request."})
        
        except Exception as e:
            # Catch any unexpected errors
            return JsonResponse({"success": False, "error": str(e)})
    
    # If the request method is not POST, return an error
    return JsonResponse({"success": False, "error": "Invalid request method."})




# @login_required
# def setup_job_seeker_profile(request):
#     try:
#         profile = request.user.job_seeker_profile
#     except ObjectDoesNotExist:
#         profile = JobSeekerProfile(user=request.user)

#     # Fetch choices for industries, provinces, and schools/universities
#     industry_choices = JobSeekerProfile.INDUSTRY_CHOICES
#     province_choices = JobSeekerProfile.PROVINCE_CHOICES
#     school_choices = JobSeekerProfile.SCHOOL_CHOICES

#     if request.method == 'POST':
#         profile.first_name = request.POST.get('first_name')
#         profile.last_name = request.POST.get('last_name')
#         profile.profile_photo = request.FILES.get('profile_photo')
#         profile.skills = request.POST.get('skills')
#         profile.years_of_experience = request.POST.get('years_of_experience')
#         profile.phone = request.POST.get('phone')
#         profile.province = request.POST.get('province')  # Save province
#         profile.school_or_university = request.POST.get('school_or_university')  # Save school/university
#         profile.industry = request.POST.get('industry')
#         profile.save()
#         return redirect('home')

#     return render(request, 'profiles/setup/job_seeker_profile_setup.html', {
#         'profile': profile,
#         'industry_choices': industry_choices,
#         'province_choices': province_choices,
#         'school_choices': school_choices
#     })

logger = logging.getLogger(__name__)

@login_required
def setup_job_seeker_profile(request):
    try:
        profile = request.user.job_seeker_profile
    except ObjectDoesNotExist:
        profile = JobSeekerProfile(user=request.user)

    # Fetch choices for industries, provinces, and schools/universities
    industry_choices = JobSeekerProfile.INDUSTRY_CHOICES
    province_choices = JobSeekerProfile.PROVINCE_CHOICES
    school_choices = JobSeekerProfile.SCHOOL_CHOICES

    if request.method == 'POST':
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.carrier = request.POST.get('carrier')
        profile.about_me = request.POST.get('about_me')
        profile.profile_photo = request.FILES.get('profile_photo')
        profile.years_of_experience = request.POST.get('years_of_experience')
        profile.phone = request.POST.get('phone')
        profile.province = request.POST.get('province')  # Save province
        profile.school_or_university = request.POST.get('school_or_university')  # Save school/university
        profile.industry = request.POST.get('industry')

        # Save profile
        profile.save()

        # Debugging: Log the saved data
        logger.info(f"Profile saved successfully for user {request.user.username}")
        logger.info(f"Profile details: {profile.__dict__}")
        
        # Optional: Log if file was uploaded
        if profile.profile_photo:
            logger.info(f"Profile photo uploaded: {profile.profile_photo.url}")
        else:
            logger.warning("No profile photo uploaded.")

        # Display success message
        messages.success(request, "Your profile was updated successfully!")

        return redirect('home')

    return render(request, 'profiles/setup/job_seeker_profile_setup.html', {
        'profile': profile,
        'industry_choices': industry_choices,
        'province_choices': province_choices,
        'school_choices': school_choices
    })



@login_required
def view_profile(request):
    company = None
    user = request.user
    profile = None
    is_job_seeker = False
    is_employer = False
    is_company_employer = False
    is_individual_employer = True
    
    if user.role == 'job_seeker':
        profile = user.job_seeker_profile
        is_job_seeker = True
    if user.role == 'employer':
        try:
            profile = IndividualEmployerProfile.objects.get(user=request.user)
        except IndividualEmployerProfile.DoesNotExist:
            profile = None 
            is_individual_employer = False
        if profile == None:     
            company = user.employer_profile.company
            is_company_employer = True
    
    context = {
        'profile': profile,
        'is_job_seeker' : is_job_seeker,
        'is_employer' : is_employer,
        'company' : company,
        'is_company_employer' : is_company_employer,
        'is_individual_employer' : is_individual_employer
    }    
    print(is_company_employer)
    print(profile)
    return render(request, 'profiles/view/my_profile.html', context)


def select_create_company_profile(request):
    companies = Company.objects.all()
    context = {
        'companies' : companies
    }
    return render(request, 'profiles/setup/company_select_create_setup.html', context)


def search_results(request):
    pass

def select_company(request, id):
    company = get_object_or_404(Company, id=id)
    context = {
        'company' : company
    }
    return render(request, 'profiles/setup/company_confirm.html', context)


def confirm_company(request, id):
    company = get_object_or_404(Company, id=id)
    if request.method == 'POST':
        response = request.POST.get('response')
        
        if response == 'yes':
            profile = get_object_or_404(EmployerProfile, user=request.user)
            
            profile.company = company
            profile.save()
            
            print(profile.company)
            return redirect('employer_profile_setup', company_id=id) 
        if response == 'no':
            return redirect('select_create_company')
        
    return render(request, 'profiles/setup/company_confirm.html')



def choose_company(request, id):
    company = get_object_or_404(Company, id=id)

    return render(request, 'profiles/setup/company_confirm.html', {'company' : company})
    
    
def company_selection(request):
    if request.method == 'POST':
        # Get the company ID from the POST data
        company_id = request.POST.get('company_id')

        if company_id:
            # Try to get the company object using the company_id
            company = get_object_or_404(Company, id=company_id)
            print(company)
    return render(request, 'profiles/setup/company_confirm.html')


from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required
def setup_employer_profile(request, company_id):
    company = get_object_or_404(Company, id=company_id)
    print(f"-----------{company}")
    
    try:
        profile = request.user.employer_profile
        print(profile)
    except ObjectDoesNotExist:
        profile = EmployerProfile(user=request.user)
        profile.save()  # Make sure to save the profile object initially
        print("Profile Does not exist")

    if request.method == 'POST':
        # Get values from the form
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        position = request.POST.get('position')
        phone = request.POST.get('phone')
        profile_photo = request.FILES.get('profile_photo')

        # Print out the received values for debugging
        print("First Name:", first_name)
        print("Last Name:", last_name)
        print("Position:", position)
        print("Phone:", phone)
        print("Profile Photo:", profile_photo)

        # Here you can validate or inspect the values as needed

        # Assign values to the profile model
        profile.first_name = first_name
        profile.last_name = last_name
        profile.position = position
        profile.phone = phone
        profile.profile_photo = profile_photo
        profile.company = company
        
        # Save the profile after assignment
        profile.save()

        # Redirect to the company selection/creation page after profile setup
        return redirect('home')

    return render(request, 'profiles/setup/employer_profile_setup.html', {'profile': profile})



def setup_individual_employer_profile(request):
    try:
        profile = request.user.individual_employer_profile
    except ObjectDoesNotExist:
        profile = IndividualEmployerProfile(user=request.user)

    if request.method == 'POST':
        # Manually retrieve form data
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        location = request.POST.get('location', '')
        is_admin = 'is_admin' in request.POST  # Checkbox returns as present or not

        # Handle file upload
        profile_photo = request.FILES.get('profile_photo', None)

        # Update profile fields
        profile.first_name = first_name
        profile.last_name = last_name
        profile.email = email
        profile.phone = phone
        profile.location = location
        profile.is_admin = is_admin
        if profile_photo:
            profile.profile_photo = profile_photo

        # Save profile
        profile.save()

        # Redirect after saving
        return redirect('home')
    return render(request, 'profiles/setup/individual_employer_setup.html', {'profile': profile})


@login_required  # Ensure the user is logged in to create a company
def setup_company_profile(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        industry = request.POST.get('industry')
        logo = request.FILES.get('logo')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        website = request.POST.get('website')
        size = request.POST.get('size')
        headquarters = request.POST.get('headquarters')
        is_active = request.POST.get('is_active') == "True"

        # Create a new company instance
        company = Company(
            name=name,
            description=description,
            industry=industry,
            logo=logo,
            admin = request.user,
            address=address,
            phone_number=phone_number,
            email=email,
            website=website,
            size=size,
            headquarters=headquarters,
            is_active=is_active,
        )
        
        company.save()
        return redirect('employer_profile_setup', company_id=company.id) # Redirect to a success page or list view
    
    return render(request, 'profiles/setup/company_profile_setup.html')


def view_js_dashboard(request):
    return render(request, 'profiles/dashboard/job_seeker_dashboard.html')

def test(request):
    if request.method == 'POST':
        employer_type = request.POST['employer_type']
        print(employer_type)
        
    return render(request, 'profiles/setup/employer_type_selection.html')


def select_employer_type(request):
    if request.method == 'POST':
        employer_type = request.POST.get('employer_type')

        try:
            # Check if employer_type is either 'company' or 'individual'
            if employer_type in ['company', 'individual']:
                # For Company Employer
                if employer_type == 'company':
                    # Check if the user already has an EmployerProfile
                    if not EmployerProfile.objects.filter(user=request.user).exists():
                        company_employer_profile = EmployerProfile.objects.create(
                            user=request.user,
                            is_company_employer=True
                        )
                        print(company_employer_profile)
                        # Redirect to the company profile setup page
                        return redirect('select_create_company')
                    else:
                        messages.error(request, 'You already have a company employer profile.')

                # For Individual Employer
                elif employer_type == 'individual':
                    # Check if the user already has an IndividualEmployerProfile
                    if not IndividualEmployerProfile.objects.filter(user=request.user).exists():
                        individual_employer_profile = IndividualEmployerProfile.objects.create(
                            user=request.user,
                            is_individual_employer=True
                        )
                        
                        # Redirect to the individual profile setup page
                        return redirect('individual_profile_setup')
                    else:
                        messages.error(request, 'You already have an individual employer profile.')

            else:
                # Invalid employer_type
                messages.error(request, 'Invalid selection. Please try again.')

        except IntegrityError:
            messages.error(request, 'An error occurred while creating your profile. Please try again.')
        
    else:
        print("GET request")
    
    return render(request, 'accounts/employer_type_selection.html')


def view_user_profile(request, id):
    user_profile = JobSeekerProfile.objects.get(id=id)
    skills = Skill.objects.filter(job_seeker_profile=user_profile)
    print(f"Skills {skills}")
    experiences = GeneralExperience.objects.filter(job_seeker_profile=user_profile)
    print(f"Experiences {experiences}")
    
    context = {
        'user_profile': user_profile,
        'skills' : skills,
        'experiences' : experiences
    }
    
    return render(request, 'profiles/view/user_profile.html', context)





def view_company_profile(request):
    
    return render(request, 'profiles/view/company_profile.html')