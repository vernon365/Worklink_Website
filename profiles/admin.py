from django.contrib import admin
from .models import EmployerProfile, JobSeekerProfile, Company, CompanyEmployer, IndividualEmployerProfile, Skill, GeneralExperience


admin.site.register(EmployerProfile)
admin.site.register(IndividualEmployerProfile)
admin.site.register(JobSeekerProfile)
admin.site.register(Company)
admin.site.register(CompanyEmployer)
admin.site.register(Skill)
admin.site.register(GeneralExperience)
