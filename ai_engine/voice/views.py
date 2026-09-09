import json

from django.http import JsonResponse

from ai_engine.services.command_handler import handle_command


def process_voice_command(request):

    if request.method != "POST":

        return JsonResponse(
            {
                "success": False,
                "error": "Only POST requests are allowed."
            },
            status=405
        )

    try:

        data = json.loads(request.body)

        command = data.get(
            "command",
            ""
        )

        patient_id = data.get(
            "patient_id"
        )

        language = data.get(
            "language",
            "en"
        )

        result = handle_command(
            command,
            patient_id,
            language
        )

        return JsonResponse(result)

    except Exception as error:

        return JsonResponse(
            {
                "success": False,
                "error": str(error)
            },
            status=400
        )