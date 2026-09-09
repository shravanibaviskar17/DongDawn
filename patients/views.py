from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from .models import Patient
from reminders.models import Reminder
from games.models import GameResult


def patient_list(request):

    patients = Patient.objects.all().order_by('name')

    return render(
        request,
        'patients/patient_list.html',
        {
            'patients': patients
        }
    )


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
                        "error": "This account is not linked to a patient."
                    }
                )

        else:

            return render(
                request,
                "patients/patient_login.html",
                {
                    "error": "Invalid username or password."
                }
            )

    return render(
        request,
        "patients/patient_login.html"
    )


def patient_logout(request):

    logout(request)

    return redirect("patient_login")