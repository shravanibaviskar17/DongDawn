from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.caregiver_dashboard,
        name='caregiver_dashboard'
    ),
]