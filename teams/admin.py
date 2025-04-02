from django.contrib import admin
from .models import Team, TeamJobseeker, TeamJoinRequest


admin.site.register(Team)
admin.site.register(TeamJobseeker)
admin.site.register(TeamJoinRequest)
