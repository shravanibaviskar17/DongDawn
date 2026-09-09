
from reminders.models import Reminder

from .language_service import get_language
from .response_service import (
    format_reminder_response,
    game_response,
    unknown_response
)


def normalize_command(command):

    if not command:
        return ""

    return command.strip().lower()


def handle_command(
    command,
    patient_id,
    language="en"
):

    language = get_language(language)

    command = normalize_command(command)

    if not patient_id:

        return {
            "success": False,
            "response": "Patient ID is required."
        }


    # --------------------------------------------------------
    # MEDICINE / REMINDER COMMAND
    # --------------------------------------------------------

    medicine_words = [
        "medicine",
        "medication",
        "tablet",
        "दवाई",
        "दवा",
        "औषध",
        "गोळी",
        "औषधाची"
    ]

    reminder_words = [
        "reminder",
        "reminders",
        "याद",
        "रिमाइंडर",
        "आठवण"
    ]

    if any(
        word in command
        for word in medicine_words + reminder_words
    ):

        reminder = (
            Reminder.objects
            .filter(
                patient_id=patient_id,
                is_completed=False
            )
            .order_by(
                "reminder_date",
                "reminder_time"
            )
            .first()
        )

        if reminder:

            return {
                "success": True,
                "intent": "reminder",
                "response": format_reminder_response(
                    reminder,
                    language
                )
            }

        if language == "hi":
            response = "आपकी कोई लंबित रिमाइंडर नहीं है।"

        elif language == "mr":
            response = "तुमच्याकडे कोणतेही प्रलंबित रिमाइंडर नाहीत."

        else:
            response = "You do not have any pending reminders."

        return {
            "success": True,
            "intent": "reminder",
            "response": response
        }


    # --------------------------------------------------------
    # GAME COMMAND
    # --------------------------------------------------------

    game_words = [
        "game",
        "play",
        "गेम",
        "खेल",
        "खेळ",
        "सुरू करा",
        "शुरू"
    ]

    if any(
        word in command
        for word in game_words
    ):

        return {
            "success": True,
            "intent": "game",
            "response": game_response(language),
            "redirect": f"/games/?patient_id={patient_id}"
        }


    # --------------------------------------------------------
    # UNKNOWN COMMAND
    # --------------------------------------------------------

    return {
        "success": True,
        "intent": "unknown",
        "response": unknown_response(language)
    }
