
LANGUAGES = {
    "en": {
        "name": "English",
        "speech_code": "en-IN"
    },

    "hi": {
        "name": "हिन्दी",
        "speech_code": "hi-IN"
    },

    "mr": {
        "name": "मराठी",
        "speech_code": "mr-IN"
    }
}


TRANSLATIONS = {

    "welcome": {
        "en": "Hello! How can I help you today?",
        "hi": "नमस्ते! मैं आज आपकी कैसे मदद कर सकता हूँ?",
        "mr": "नमस्कार! मी आज तुमची कशी मदत करू शकतो?"
    },

    "listening": {
        "en": "I am listening...",
        "hi": "मैं सुन रहा हूँ...",
        "mr": "मी ऐकत आहे..."
    },

    "no_reminder": {
        "en": "You do not have any pending reminders.",
        "hi": "आपकी कोई लंबित रिमाइंडर नहीं है।",
        "mr": "तुमच्याकडे कोणतेही प्रलंबित रिमाइंडर नाहीत."
    },

    "medicine": {
        "en": "Your next medicine reminder is",
        "hi": "आपकी अगली दवाई का रिमाइंडर है",
        "mr": "तुमच्या पुढील औषधाची आठवण आहे"
    },

    "game": {
        "en": "Let's start your cognitive game.",
        "hi": "आइए आपका कॉग्निटिव गेम शुरू करते हैं।",
        "mr": "चला तुमचा कॉग्निटिव गेम सुरू करूया."
    },

    "unknown": {
        "en": "I can help you with reminders, medicines and cognitive games.",
        "hi": "मैं रिमाइंडर, दवाई और कॉग्निटिव गेम में आपकी मदद कर सकता हूँ।",
        "mr": "मी रिमाइंडर, औषधे आणि कॉग्निटिव गेममध्ये तुमची मदत करू शकतो."
    }
}


def get_language(language):
    if language not in LANGUAGES:
        return "en"

    return language


def get_translation(key, language="en"):

    language = get_language(language)

    return TRANSLATIONS.get(
        key,
        TRANSLATIONS["unknown"]
    ).get(
        language,
        TRANSLATIONS["unknown"]["en"]
    )
