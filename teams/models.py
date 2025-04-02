from django.db import models
from accounts.models import CustomUser

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_teams')
    team_logo = models.ImageField(upload_to='team_logos/', blank=True, null=True)  # New field for the team logo
    
    def __str__(self):
        return self.name if self.name else "Unnamed Team"

    def get_member_count(self):
        return self.team_members.count()
    
    def is_admin(self, user):
        return self.created_by == user
    
    def delete(self, *args, **kwargs):
    # Optionally: delete related team members and join requests explicitly
        self.team_members.all().delete()
        self.join_requests.all().delete()
        super(Team, self).delete(*args, **kwargs)



class TeamJobseeker(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('member', 'Normal Member'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_members')
    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default='member')  # Specify choices and default role
    joined_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        # Ensure that even if username or team name is None, it returns a valid string
        username = self.user.username if self.user.username else "Unknown User"
        team_name = self.team.name if self.team.name else "Unnamed Team"
        return f'{username} - {team_name} ({self.get_role_display()})'



# New model for join requests
class TeamJoinRequest(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='join_requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Request from {self.user.username} to join {self.team.name if self.team.name else "Unnamed Team"}'

    
# Method to accept the request
    def accept(self):
        self.status = self.ACCEPTED
        # Add the user to the team members
        TeamJobseeker.objects.create(user=self.user, team=self.team, role='member')  # Ensure role matches choice
        self.save()
