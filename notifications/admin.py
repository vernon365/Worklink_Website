from django.contrib import admin
from .models import EmployerNotification, TeamJoinRequestNotification, JobPostingNotification

admin.site.register(JobPostingNotification)
admin.site.register(EmployerNotification)
admin.site.register(TeamJoinRequestNotification)


