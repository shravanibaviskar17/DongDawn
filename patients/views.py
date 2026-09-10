from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils import timezone
import json

from .models import Patient, PatientLocation
from reminders.models import Reminder
from games.models import GameResult


# =========================================================
# PATIENT LIST
# =========================================================

def patient_list(request):

    patients = Patient.objects.all().order_by('name')

    return render(
        request,
        'patients/patient_list.html',
        {
            'patients': patients
        }
    )


# =========================================================
# PATIENT LOGIN
# =========================================================

def patient_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            try:

                patient = Patient.objects.get(
                    user=user
                )

                login(request, user)

                return redirect(
                    "patient_dashboard",
                    patient_id=patient.id
                )

            except Patient.DoesNotExist:

                return render(
                    request,
                    "patients/patient_login.html",
                    {
                        "error":
                        "This account is not linked to a patient."
                    }
                )

        else:

            return render(
                request,
                "patients/patient_login.html",
                {
                    "error":
                    "Invalid username or password."
                }
            )

    return render(
        request,
        "patients/patient_login.html"
    )


# =========================================================
# PATIENT LOGOUT
# =========================================================

def patient_logout(request):

    logout(request)

    return redirect("patient_login")


# =========================================================
# PATIENT DASHBOARD
# =========================================================

def patient_dashboard(request, patient_id):

    patient = Patient.objects.get(
        id=patient_id
    )

    reminders = Reminder.objects.filter(
        patient=patient,
        is_completed=False
    ).order_by(
        'reminder_time'
    )

    game_results = GameResult.objects.filter(
        patient=patient
    ).order_by(
        '-played_at'
    )[:5]

    return render(
        request,
        'patients/patient_dashboard.html',
        {
            'patient': patient,
            'reminders': reminders,
            'game_results': game_results,
        }
    )


# =========================================================
# LOCATION CONSENT
# =========================================================

def give_location_consent(request, patient_id):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "error":
                "Only POST requests are allowed."
            },
            status=405
        )

    try:

        patient = Patient.objects.get(
            id=patient_id
        )

        location, created = PatientLocation.objects.get_or_create(
            patient=patient,
            defaults={
                "latitude": 0,
                "longitude": 0
            }
        )

        location.consent_given = True
        location.is_shared = True
        location.consent_given_at = timezone.now()

        location.save()

        return JsonResponse(
            {
                "success": True,
                "message":
                "Location sharing consent enabled."
            }
        )

    except Patient.DoesNotExist:

        return JsonResponse(
            {
                "success": False,
                "error":
                "Patient not found."
            },
            status=404
        )


# =========================================================
# STOP LOCATION SHARING
# =========================================================

def stop_location_sharing(request, patient_id):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "error":
                "Only POST requests are allowed."
            },
            status=405
        )

    try:

        location = PatientLocation.objects.get(
            patient_id=patient_id
        )

        location.is_shared = False

        location.save()

        return JsonResponse(
            {
                "success": True,
                "message":
                "Location sharing stopped."
            }
        )

    except PatientLocation.DoesNotExist:

        return JsonResponse(
            {
                "success": False,
                "error":
                "Location sharing is not enabled."
            },
            status=404
        )


# =========================================================
# UPDATE PATIENT LOCATION
# =========================================================

def update_patient_location(request, patient_id):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "error":
                "Only POST requests are allowed."
            },
            status=405
        )

    try:

        location = PatientLocation.objects.get(
            patient_id=patient_id
        )

        # Check consent before accepting location
        if (
            not location.consent_given
            or not location.is_shared
        ):

            return JsonResponse(
                {
                    "success": False,
                    "error":
                    "Location sharing consent is required."
                },
                status=403
            )

        # Read JSON data
        data = json.loads(
            request.body
        )

        latitude = data.get(
            "latitude"
        )

        longitude = data.get(
            "longitude"
        )

        accuracy = data.get(
            "accuracy"
        )

        # Validate coordinates
        if (
            latitude is None
            or longitude is None
        ):

            return JsonResponse(
                {
                    "success": False,
                    "error":
                    "Latitude and longitude are required."
                },
                status=400
            )

        # Save latest location
        location.latitude = latitude

        location.longitude = longitude

        location.accuracy = accuracy

        location.save()

        return JsonResponse(
            {
                "success": True,
                "message":
                "Latest location updated successfully.",
                "updated_at":
                location.updated_at.isoformat()
            }
        )

    except PatientLocation.DoesNotExist:

        return JsonResponse(
            {
                "success": False,
                "error":
                "Location sharing is not enabled."
            },
            status=404
        )

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "success": False,
                "error":
                "Invalid JSON data."
            },
            status=400
        )

    except Exception as error:

        return JsonResponse(
            {
                "success": False,
                "error":
                str(error)
            },
            status=400
        )