from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.patient_list,
        name='patient_list'
    ),

    path(
        'login/',
        views.patient_login,
        name='patient_login'
    ),

    path(
        'logout/',
        views.patient_logout,
        name='patient_logout'
    ),

    path(
        'dashboard/<int:patient_id>/',
        views.patient_dashboard,
        name='patient_dashboard'
    ),

]