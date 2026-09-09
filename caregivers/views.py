from django.shortcuts import render
from patients.models import Patient
from games.models import GameResult
from reminders.models import Reminder
from django.db.models import Avg, Max


def caregiver_dashboard(request):

    patients = Patient.objects.all().order_by('name')

    selected_patient = None
    game_results = []
    reminders = []

    total_games = 0
    average_score = 0
    average_accuracy = 0
    best_score = 0
    latest_difficulty = "Not available"

    chart_labels = []
    chart_accuracy = []
    chart_scores = []

    patient_id = request.GET.get('patient_id')

    if patient_id:

        try:

            selected_patient = Patient.objects.get(
                id=patient_id
            )

            # -----------------------------
            # GAME RESULTS
            # -----------------------------

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

                best_score = statistics['best_score'] or 0

                latest_difficulty = (
                    game_results.first().difficulty
                )

                # Chart data
                results_for_chart = list(
                    reversed(game_results)
                )

                for result in results_for_chart:

                    chart_labels.append(
                        result.played_at.strftime('%d %b')
                    )

                    chart_accuracy.append(
                        result.accuracy
                    )

                    chart_scores.append(
                        result.score
                    )

            # -----------------------------
            # REMINDERS
            # -----------------------------

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
        'caregivers/dashboard.html',
        {
            'patients': patients,

            'selected_patient': selected_patient,

            'game_results': game_results,

            'reminders': reminders,

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