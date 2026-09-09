from django.http import JsonResponse
from games.models import GameResult


def calculate_difficulty(accuracy):

    accuracy = float(accuracy)

    if accuracy < 50:
        return "easy"

    elif accuracy < 80:
        return "medium"

    else:
        return "hard"


def get_next_difficulty(request):

    patient_id = request.GET.get('patient_id')

    if not patient_id:

        return JsonResponse(
            {
                "success": False,
                "error": "Patient ID is required."
            },
            status=400
        )

    latest_result = (
        GameResult.objects
        .filter(patient_id=patient_id)
        .order_by('-played_at')
        .first()
    )

    if latest_result is None:

        difficulty = "easy"

    else:

        difficulty = calculate_difficulty(
            latest_result.accuracy
        )

    return JsonResponse(
        {
            "success": True,
            "difficulty": difficulty
        }
    )