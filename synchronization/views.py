from django.shortcuts import render
from .models import Patient


def patient_list(request):

    patients = Patient.objects.all().order_by('name')

    return render(
        request,
        'patients/patient_list.html',
        {
            'patients': patients
        }
    )