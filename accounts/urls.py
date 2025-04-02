from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views._logout, name='logout'),
    path('role-selection', views.select_role, name='role_selection'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),  # Add your forgot password view
]