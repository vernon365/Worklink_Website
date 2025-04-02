from django.urls import path
from . import views


urlpatterns = [
    path('setup/job-seeker/', views.setup_job_seeker_profile, name='setup_job_seeker_profile'),
    path('view-profile/', views.view_profile, name='view_profile'),
    # path('v-view-profile/<int:pid>', views.visitor_view_profile, name='visitor_view_profile'),
    path('setup/employer-company', views.select_create_company_profile, name='select_create_company'),
    path('company-selection/<int:id>', views.select_company, name='company_selection'),
    path('choose_company/<int:id>', views.choose_company, name='choose_company'),
    path('confirm_company/<int:id>', views.confirm_company, name='confirm_company'),
    path('search', views.search_results, name='search_results'),
    path('setup/employer/<int:company_id>', views.setup_employer_profile, name='employer_profile_setup'),
    path('setup/employer/individual', views.setup_individual_employer_profile, name='individual_profile_setup'),
    path('setup/company-profile', views.setup_company_profile, name='company_profile_setup'),
    path('jobseeker/dashboard', views.view_js_dashboard, name='view_js_dashbaord'),
    path('employer-type-selection', views.select_employer_type, name='employer_type_selection'),
    path('view-user-profile/<int:id>', views.view_user_profile, name='view_user_profile'),
    path('get-skills/', views.get_skills, name='get_skills'),
    path('save-skills/', views.save_skills, name='save_skills'),
    path('get_experiences/', views.get_experiences, name='get_experiences'),
    path('save-experiences/', views.save_experiences, name='save_experiences'),
    path('remove-experience/', views.remove_experience, name='remove_experience'),
    path('add_experience/', views.add_experience, name='add_experience'),
    path('company-profile-view', views.view_company_profile, name='company_profile_view')
]