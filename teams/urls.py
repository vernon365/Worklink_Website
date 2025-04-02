from django.urls import path
from . import views

urlpatterns = [
    path('confirm-message/<int:r_id>/', views.get_confirm_page, name='confirm_message'),
    path('create-team/', views.create_team, name='create_team'),
    path('teams_list/', views.view_teams, name='team_list'),
    path('team-detail/<int:team_id>/', views.view_team_details, name='team_details'),
    path('team-join-request/<int:team_id>/', views.join_request, name='join_request'),
    path('confirm-team-join-request/<int:rid>/', views.confirm_team_join, name='confirm_team_join'),
    path('add-member/<int:t_id>', views.add_members, name='add_members'),
]
