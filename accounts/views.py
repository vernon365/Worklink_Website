from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth import authenticate, logout as auth_logout, get_user_model
from django.contrib import messages
from profiles.models import JobSeekerProfile, EmployerProfile, Company
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import PasswordResetForm  # Make sure to create this form
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from .forms import PasswordResetForm 
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from .models import CustomUser
import logging

Users = get_user_model()
#  Registration view
logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        logger.debug("Register view hit with POST request.")
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Check if the email already exists
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'success': False, 'error': 'Email already exists.'})

        # Check if passwords match
        if password1 != password2:
            return JsonResponse({'success': False, 'error': 'Passwords do not match.'})

        # Create user manually
        user = CustomUser.objects.create_user(email=email, password=password1, username=email)

        # Authenticate the user
        authenticated_user = authenticate(request, username=email, password=password1)

        if authenticated_user is not None:
            # Log the user in
            auth_login(request, authenticated_user)
            logger.debug(f"User {email} successfully logged in after registration.")
            return JsonResponse({'success': True, 'redirect_url': 'accounts/role-selection'})  # Redirect URL can be updated as needed
        else:
            return JsonResponse({'success': False, 'error': 'Authentication failed.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})

# Login view
def login_view(request):
    if request.method == 'POST':
        # Print out the received POST data
        print("Received POST data:", request.POST)
        
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Return JSON for success and redirect URL
            return JsonResponse({'success': True, 'redirect_url': ''})
        else:
            # Print out form errors for debugging
            print("Form errors:", form.errors)
            # Return JSON for error in login
            return JsonResponse({'success': False, 'error': 'Invalid username or password.'})
    else:
        # Print a message for GET requests
        print("GET request received. Login not permitted via GET request.")
        return JsonResponse({'success': False, 'error': 'Login not permitted via GET request'})


# Logout view
def _logout(request):
    auth_logout(request)
    return redirect('home')  # Redirect to login page after logout

# Forgot Password view
def forgot_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Implement password reset logic here (e.g., sending a password reset email)
            messages.success(request, 'Password reset instructions have been sent to your email.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid email address.')
    else:
        form = PasswordResetForm()
    return render(request, 'registration/forgot_password.html', {'form': form})


def select_role(request):
    if request.method == 'POST':
        role = request.POST.get('role')
        user = request.user
        user.role = role
        user.save()

        if role == 'job_seeker':
            JobSeekerProfile.objects.get_or_create(user=user)
            return redirect('setup_job_seeker_profile')
        elif role == 'employer':
            return redirect('employer_type_selection')
        
    return render(request, 'accounts/role_selection.html')


def employer_type_selection(request):
    if request.method == 'POST':
        employer_type = request.POST.get('employer_type')
        
        try:
            profile = EmployerProfile.objects.get(user=request.user)

            if employer_type in ['company', 'individual']:
                profile.employer_type = employer_type
                profile.save()
                
                if employer_type == 'company':
                    return redirect('select_create_company')
                elif employer_type == 'individual':
                    return redirect('individual_profile_setup')
            else:
                messages.error(request, 'Invalid selection. Please try again.')

        except EmployerProfile.DoesNotExist:
            messages.error(request, 'Employer profile not found. Please try again.')
    else:
        print("get request")
    return render(request, 'accounts/employer_type_selection.html')

def forgot_password(request):
    pass


def test(request):
    print(request.user)
    user = request.user
    
    if user.is_authenticated:
        print("Yes")
    else:
        print('no')
    return redirect('home')


