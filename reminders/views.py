from django.shortcuts import render, redirect, get_object_or_404
from patients.models import Patient
from .models import Reminder


def reminder_dashboard(request):

    patients = Patient.objects.all().order_by('name')

    selected_patient = None
    reminders = []

    patient_id = request.GET.get('patient_id')

    if patient_id:

        try:
            selected_patient = Patient.objects.get(
                id=patient_id
            )

            reminders = Reminder.objects.filter(
                patient=selected_patient
            ).order_by(
                'reminder_date',
                'reminder_time'
            )

        except Patient.DoesNotExist:

            selected_patient = None

    return render(
        request,
        'reminders/dashboard.html',
        {
            'patients': patients,
            'selected_patient': selected_patient,
            'reminders': reminders,
        }
    )


def patient_reminders(request, patient_id):

    try:
        patient = Patient.objects.get(
            id=patient_id
        )

    except Patient.DoesNotExist:

        return render(
            request,
            'reminders/patient_reminders.html',
            {
                'patient': None,
                'reminders': []
            }
        )

    reminders = Reminder.objects.filter(
        patient=patient
    ).order_by(
        'reminder_date',
        'reminder_time'
    )

    return render(
        request,
        'reminders/patient_reminders.html',
        {
            'patient': patient,
            'reminders': reminders
        }
    )


def complete_reminder(request, reminder_id):

    if request.method == 'POST':

        reminder = get_object_or_404(
            Reminder,
            id=reminder_id
        )

        reminder.is_completed = True

        reminder.save()

        return redirect(
            'patient_reminders',
            patient_id=reminder.patient.id
        )

    return redirect(
        'reminder_dashboard'
    )