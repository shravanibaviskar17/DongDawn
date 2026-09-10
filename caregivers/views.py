from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max

from patients.models import Patient, PatientLocation
from games.models import GameResult
from reminders.models import Reminder
from .models import Caregiver


@login_required
def caregiver_dashboard(request):

    # -------------------------------------------------
    # Find caregiver connected to logged-in user
    # -------------------------------------------------

    try:

        caregiver = Caregiver.objects.get(
            user=request.user
        )

    except Caregiver.DoesNotExist:

        return render(
            request,
            'caregivers/dashboard.html',
            {
                'patients': [],
                'selected_patient': None,
                'game_results': [],
                'reminders': [],
                'location': None,
                'total_games': 0,
                'average_score': 0,
                'average_accuracy': 0,
                'best_score': 0,
                'latest_difficulty': 'Not available',
                'chart_labels': [],
                'chart_accuracy': [],
                'chart_scores': [],
                'error': 'No caregiver profile is linked to this account.'
            }
        )


    # -------------------------------------------------
    # Only patients assigned to this caregiver
    # -------------------------------------------------

    patients = caregiver.patients.all().order_by('name')


    selected_patient = None

    game_results = []

    reminders = []

    location = None


    total_games = 0

    average_score = 0

    average_accuracy = 0

    best_score = 0

    latest_difficulty = "Not available"


    chart_labels = []

    chart_accuracy = []

    chart_scores = []


    # -------------------------------------------------
    # Selected patient
    # -------------------------------------------------

    patient_id = request.GET.get('patient_id')


    if patient_id:

        try:

            # IMPORTANT:
            # Only allow this caregiver's assigned patients

            selected_patient = patients.get(
                id=patient_id
            )


            # -------------------------------------------------
            # GAME RESULTS
            # -------------------------------------------------

            game_results = GameResult.objects.filter(
                patient=selected_patient
            ).order_by('-played_at')


            total_games = game_results.count()


            if total_games > 0:

                statistics = game_results.aggregate(

                    average_score=Avg('score'),

                    average_accuracy=Avg('accuracy'),

                    best_score=Max('score')

                )


                average_score = round(
                    statistics['average_score'] or 0,
                    2
                )


                average_accuracy = round(
                    statistics['average_accuracy'] or 0,
                    2
                )


                best_score = (
                    statistics['best_score'] or 0
                )


                latest_difficulty = (
                    game_results.first().difficulty
                )


                # -------------------------------------------------
                # CHART DATA
                # -------------------------------------------------

                results_for_chart = list(
                    reversed(game_results)
                )


                for result in results_for_chart:

                    chart_labels.append(
                        result.played_at.strftime(
                            '%d %b'
                        )
                    )


                    chart_accuracy.append(
                        result.accuracy
                    )


                    chart_scores.append(
                        result.score
                    )


            # -------------------------------------------------
            # REMINDERS
            # -------------------------------------------------

            reminders = Reminder.objects.filter(
                patient=selected_patient
            ).order_by(
                'reminder_date',
                'reminder_time'
            )


            # -------------------------------------------------
            # LATEST LOCATION
            # -------------------------------------------------

            try:

                location = PatientLocation.objects.get(
                    patient=selected_patient
                )

            except PatientLocation.DoesNotExist:

                location = None


        except Patient.DoesNotExist:

            selected_patient = None


    # -------------------------------------------------
    # RENDER DASHBOARD
    # -------------------------------------------------

    return render(

        request,

        'caregivers/dashboard.html',

        {

            'caregiver': caregiver,

            'patients': patients,

            'selected_patient': selected_patient,

            'game_results': game_results,

            'reminders': reminders,

            'location': location,

            'total_games': total_games,

            'average_score': average_score,

            'average_accuracy': average_accuracy,

            'best_score': best_score,

            'latest_difficulty': latest_difficulty,

            'chart_labels': chart_labels,

            'chart_accuracy': chart_accuracy,

            'chart_scores': chart_scores,

        }

    )