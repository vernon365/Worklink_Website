from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Team, TeamJobseeker, TeamJoinRequest
from notifications.models import TeamJoinRequestNotification
from accounts.models import CustomUser



    


@login_required
def create_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        description = request.POST.get('description')
        specialization = request.POST.get('specialization')  # Correctly fetch specialization
        created_by = request.user  # The logged-in user is the team admin
        team_logo = request.FILES.get('team_logo')  # Get the uploaded team logo

        # Validate required fields
        if not team_name:
            return HttpResponse("Team name is required", status=400)

        if not created_by:
            return HttpResponse("Admin is required", status=400)

        # Create the team instance
        team = Team.objects.create(
            name=team_name,
            description=description,
            specialization=specialization,  # Use the specialization provided by the form
            created_by=created_by,
            team_logo=team_logo  # Can be None if no logo is uploaded
        )

        # Add the creator as an admin member of the team
        TeamJobseeker.objects.create(
            user=request.user,
            team=team,
            role='admin'
        )

        return redirect('team_list')  # Redirect to the team list view

    return render(request, 'teams/create_team.html')  # Render the creation form



def view_teams(request):
    teams = Team.objects.all()
    context = {
        'teams' : teams
    }
    
    return render(request, 'teams/view_teams.html', context)


def view_team_details(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    team_members = TeamJobseeker.objects.filter(team=team)
    all_requests = TeamJoinRequest.objects.all()
    my_request = None
    
    for r in all_requests:
        if r.user == request.user and r.team == team:
            my_request = r

    
    team_requests = TeamJoinRequest.objects.filter(team=team, status='pending')
    
    for re in team_requests:
        print(re)
        print(f"status {re.status}")
        print("")
            
    print(f"team request {team_requests.count()}")
    
    context = {
        'team' : team,
        'team_members' : team_members,
        'my_request' : my_request,
        'team_requests' : team_requests
    }
    
    return render(request, 'teams/team_details.html', context)




def join_request(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    
    # Check if the user is already a member of the team
    existing_request = TeamJoinRequest.objects.filter(user=request.user, team=team).first()
    message = f"{request.user} - has requested to join {team}"
    if not existing_request:
        # Create the new team join request
        r = TeamJoinRequest.objects.create(
            user=request.user,
            team=team,

        )

        # Create the notification only if a new request is created
        n = TeamJoinRequestNotification.objects.create(
            user=team.created_by,
            team=team,
            message = message 
        )

    # List the current team members (for debugging purposes)
    members = TeamJobseeker.objects.filter(team=team)
    for m in members:
        print(m)

    return render(request, 'teams/join_request.html')



def confirm_team_join(request, rid):
    print("-----------------------")
    referer = request.META.get('HTTP_REFERER')
    re = get_object_or_404(TeamJoinRequest, id=rid)
    team = re.team
    requester = re.user

    if request.method == 'POST':
        referer = request.META.get('HTTP_REFERER')
        print("yes its a post")
        re.status = 'accepted'
        re.save()
        message = f"Your request to join {team} has been {re.status}"
        existing_member = TeamJobseeker.objects.filter(user=requester, team=team).first()

        if not existing_member:
            new_member = TeamJobseeker.objects.create(
                user=requester,
                team=team
            )
            new_member.save()

            n = TeamJoinRequestNotification.objects.create(
                user=requester,
                team=team,
                message=message
            )
            n.save()
            
        return redirect(referer)
            
        # Redirect to the team details page, passing the team ID
    return render(request, 'teams/team_details.html')



def get_confirm_page(request, r_id):

    join_request = get_object_or_404(TeamJoinRequest, id=r_id)

    
    context = {
        'join_request': join_request
    }
    return render(request, 'teams/confirm_team_join.html', context)





def add_members(request, t_id):
    team = get_object_or_404(Team, id=t_id)
    existing_members = TeamJobseeker.objects.filter(team=team).values_list('user_id', flat=True)
    users = CustomUser.objects.filter(role='job_seeker').exclude(id__in=existing_members)
    
    if request.method == 'POST':
        selected_members = request.POST.getlist('selected_members')  # Get selected members' IDs
        
        # Process the selected member IDs (e.g., add them to the team)
        for member_id in selected_members:
            # Create TeamJobseeker instance
            new_member = TeamJobseeker.objects.create(user_id=member_id, team=team)

            # Create a notification for the new member
            message = f"You have been added to the team: {team.name}."
            TeamJoinRequestNotification.objects.create(
                user=new_member.user,  # The user who has been added
                team=team,
                message=message,
            )

        # Redirect to the team details view with the team ID
        return redirect('team_details', team_id=t_id)

    context = {
        'job_seekers': users
    }
    return render(request, 'teams/add_members.html', context)