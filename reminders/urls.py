from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.reminder_dashboard,
        name='reminder_dashboard'
    ),

    path(
        'patient/<int:patient_id>/',
        views.patient_reminders,
        name='patient_reminders'
    ),

]