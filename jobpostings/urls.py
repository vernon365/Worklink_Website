from django.urls import path
from . import views

urlpatterns = [
    path('create_job_posting/', views.create_job_posting, name='create_job_posting'),
    path('list_job_postings/', views.list_job_postings, name='job_postings'),
    path('edit/<int:job_id>/', views.edit_job_posting, name='edit_job_posting'),
    path('delete/<int:job_id>/', views.delete_job_posting, name='delete_job_posting'),
    path('view-job-details/<int:job_id>', views.view_detail_job_posting, name='view_detail_job_posting'),
    path('save-job/<int:job_id>', views.save_job, name='save_job'),
    path('employer-view-job<int:job_id>', views.employer_view_job, name='employer_view_job'),
    path('fetch-jobs', views.fetch_jobs, name='fetch_jobs'),

]
