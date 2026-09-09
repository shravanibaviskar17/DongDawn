from django.contrib import admin
from django.urls import path, include


urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include('activities.urls')),

    path('accounts/', include('accounts.urls')),

    path('patients/', include('patients.urls')),

    path('games/', include('games.urls')),

    path('caregivers/', include('caregivers.urls')),

    path('reminders/', include('reminders.urls')),

    path('analytics/', include('analytics.urls')),

    path('ai/', include('ai_engine.urls')),

]