from django.contrib import admin
from django.urls import path, include
from .views import home, get_about_page, get_contact_page
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
    path('jobpostings/', include('jobpostings.urls')),
    path('applications/', include('applications.urls')),
    path('notifications/', include('notifications.urls')),
    path('teams/', include('teams.urls')),
    path('contact', get_contact_page, name='contact'),
    path('about', get_about_page, name='about')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)