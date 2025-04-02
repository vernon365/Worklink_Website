from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import update_application_status


urlpatterns = [
    path('application-succeed-message', views.application_succeed, name='apply_success'),
    path('apply/<int:job_id>/', views.apply_to_job, name='apply_to_job'),
    path('update-status/<int:application_id>/<str:status>/', views.update_application_status, name='update_application_status'),
    path('<int:id>', views.my_applications, name='my_applications'),
    path('manage_applications', views.applications, name='manage_applications'),
    path('view_applications/<int:app_id>', views.view_application, name='view_applications'),
    path('update-application-status/', update_application_status, name='update_application_status'),
    path('confirm-application/<int:id>', views.confirm_application, name='confirm_application'),
    path('reject-application/<int:id>', views.reject_application, name='reject_application'),
    # path('setup-interview/application/<int:id>', views.setup_interview, name='setup_interivew'),
    path('job_seeker-dashboard', views.view_job_seeker_db, name='job_seeker_db'),
    path('request-application-delete/<int:id>', views.request_application_delete, name='request_application_delete'),
    path('delete-application/<int:application_id>', views.delete_application, name='delete_application'),
    path('my-application-view/<int:id>', views.view_my_application, name='view_my_application')
]

    
    



