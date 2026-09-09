from django.shortcuts import render
from django.http import JsonResponse
from .models import GameResult
import json


def memory_game(request):

    patient_id = request.GET.get('patient_id')

    return render(
        request,
        'games/memory_game.html',
        {
            'patient_id': patient_id
        }
    )


def save_game_result(request):

    if request.method == 'POST':

        try:

            data = json.loads(request.body)

            game_name = data.get(
                'game_name',
                'Memory Matching'
            )

            score = data.get(
                'score',
                0
            )

            attempts = data.get(
                'attempts',
                0
            )

            accuracy = data.get(
                'accuracy',
                0
            )

            difficulty = data.get(
                'difficulty',
                'easy'
            )

            completion_time = data.get(
                'completion_time',
                0
            )

            patient_id = data.get(
                'patient_id'
            )

            if not patient_id:

                return JsonResponse(
                    {
                        'success': False,
                        'error': 'Patient ID is required.'
                    },
                    status=400
                )

            result = GameResult.objects.create(

                patient_id=patient_id,

                game_name=game_name,

                score=score,

                attempts=attempts,

                accuracy=accuracy,

                difficulty=difficulty,

                completion_time=completion_time

            )

            return JsonResponse(
                {
                    'success': True,
                    'message': 'Game result saved successfully!',
                    'result_id': result.id
                }
            )

        except Exception as e:

            return JsonResponse(
                {
                    'success': False,
                    'error': str(e)
                },
                status=400
            )

    return JsonResponse(
        {
            'success': False,
            'error': 'Only POST requests are allowed.'
        },
        status=405
    )


def routine_game(request):

    patient_id = request.GET.get(
        'patient_id'
    )

    return render(
        request,
        'games/routine_game.html',
        {
            'patient_id': patient_id
        }
    )


def object_game(request):

    patient_id = request.GET.get(
        'patient_id'
    )

    return render(
        request,
        'games/object_game.html',
        {
            'patient_id': patient_id
        }
    )
def pattern_game(request):

    patient_id = request.GET.get(
        'patient_id'
    )

    return render(
        request,
        'games/pattern_game.html',
        {
            'patient_id': patient_id
        }
    )
def emotion_game(request):

    patient_id = request.GET.get(
        'patient_id'
    )

    return render(
        request,
        'games/emotion_game.html',
        {
            'patient_id': patient_id
        }
    )
def attention_game(request):

    patient_id = request.GET.get('patient_id')

    return render(
        request,
        'games/attention_game.html',
        {
            'patient_id': patient_id
        }
    )