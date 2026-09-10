from django.urls import path
from . import views


urlpatterns = [

    # -------------------------------------------------
    # Patient pages
    # -------------------------------------------------

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


    # -------------------------------------------------
    # Location sharing
    # -------------------------------------------------

    path(
        'location/consent/<int:patient_id>/',
        views.give_location_consent,
        name='give_location_consent'
    ),

    path(
        'location/stop/<int:patient_id>/',
        views.stop_location_sharing,
        name='stop_location_sharing'
    ),

    path(
        'location/update/<int:patient_id>/',
        views.update_patient_location,
        name='update_patient_location'
    ),

]