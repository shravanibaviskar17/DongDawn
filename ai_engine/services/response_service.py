
from .language_service import get_translation


def format_reminder_response(reminder, language):

    title = reminder.title

    time_value = reminder.reminder_time.strftime("%I:%M %p")

    base = get_translation(
        "medicine",
        language
    )

    return f"{base} {time_value}. {title}."


def game_response(language):

    return get_translation(
        "game",
        language
    )


def unknown_response(language):

    return get_translation(
        "unknown",
        language
    )
