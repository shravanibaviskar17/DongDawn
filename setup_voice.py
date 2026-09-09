from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# ============================================================
# 1. CREATE FOLDERS
# ============================================================

folders = [
    BASE_DIR / "ai_engine" / "services",
    BASE_DIR / "ai_engine" / "voice",
    BASE_DIR / "ai_engine" / "templates" / "ai_engine",
    BASE_DIR / "patients" / "templates" / "patients",
    BASE_DIR / "static",
    BASE_DIR / "static" / "voice",
]

for folder in folders:
    folder.mkdir(parents=True, exist_ok=True)

print("Folders created successfully.")


# ============================================================
# 2. CREATE __init__.py FILES
# ============================================================

init_files = [
    BASE_DIR / "ai_engine" / "services" / "__init__.py",
    BASE_DIR / "ai_engine" / "voice" / "__init__.py",
]

for file_path in init_files:
    if not file_path.exists():
        file_path.write_text("", encoding="utf-8")

print("Python package files created.")


# ============================================================
# 3. LANGUAGE SERVICE
# ============================================================

language_service = r'''
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
'''

(BASE_DIR / "ai_engine" / "services" / "language_service.py").write_text(
    language_service,
    encoding="utf-8"
)


# ============================================================
# 4. RESPONSE SERVICE
# ============================================================

response_service = r'''
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
'''

(BASE_DIR / "ai_engine" / "services" / "response_service.py").write_text(
    response_service,
    encoding="utf-8"
)


# ============================================================
# 5. VOICE COMMAND HANDLER
# ============================================================

command_handler = r'''
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
'''

(BASE_DIR / "ai_engine" / "services" / "command_handler.py").write_text(
    command_handler,
    encoding="utf-8"
)


# ============================================================
# 6. VOICE API
# ============================================================

voice_api = r'''
import json

from django.http import JsonResponse

from .services.command_handler import handle_command


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

        data = json.loads(
            request.body
        )

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
'''

(BASE_DIR / "ai_engine" / "voice" / "views.py").write_text(
    voice_api,
    encoding="utf-8"
)


# ============================================================
# 7. VOICE URLS
# ============================================================

voice_urls = r'''
from django.urls import path

from . import views


urlpatterns = [

    path(
        "command/",
        views.process_voice_command,
        name="voice_command"
    ),

]
'''

(BASE_DIR / "ai_engine" / "voice" / "urls.py").write_text(
    voice_urls,
    encoding="utf-8"
)


# ============================================================
# 8. UPDATE AI ENGINE MAIN URLS
# ============================================================

ai_urls = BASE_DIR / "ai_engine" / "urls.py"

if ai_urls.exists():

    content = ai_urls.read_text(
        encoding="utf-8"
    )

    include_line = "from django.urls import path, include"

    if "from django.urls import path, include" not in content:

        content = content.replace(
            "from django.urls import path",
            include_line
        )

    if "path('voice/', include('ai_engine.voice.urls'))" not in content:

        content = content.replace(
            "urlpatterns = [",
            "urlpatterns = [\n"
            "    path('voice/', include('ai_engine.voice.urls')),"
        )

    ai_urls.write_text(
        content,
        encoding="utf-8"
    )

    print("AI Engine URLs updated.")


# ============================================================
# 9. CREATE VOICE ASSISTANT HTML
# ============================================================

voice_html = r'''
{% if patient_id %}

<section class="dd-voice-card">

    <div class="dd-voice-header">

        <div>

            <span class="dd-voice-label">
                DONGDAWN VOICE
            </span>

            <h2>
                🎙️ Talk to DongDawn
            </h2>

            <p>
                Speak naturally. I'll help you with
                reminders and cognitive activities.
            </p>

        </div>

        <div class="dd-language-box">

            <label for="ddLanguage">
                🌐 Language
            </label>

            <select
                id="ddLanguage"
                onchange="ddChangeLanguage(this.value)"
            >

                <option value="en">
                    🇮🇳 English
                </option>

                <option value="hi">
                    🇮🇳 हिन्दी
                </option>

                <option value="mr">
                    🟠 मराठी
                </option>

            </select>

        </div>

    </div>


    <div class="dd-voice-center">

        <button
            type="button"
            id="ddVoiceButton"
            class="dd-mic-button"
            onclick="ddStartListening()"
        >
            🎙️
        </button>

        <div
            id="ddVoiceStatus"
            class="dd-voice-status"
        >
            Tap the microphone and speak
        </div>

        <div
            id="ddVoiceText"
            class="dd-voice-text"
        ></div>

        <div
            id="ddVoiceResponse"
            class="dd-voice-response"
        ></div>

    </div>


    <div class="dd-voice-examples">

        <span>Try saying:</span>

        <button onclick="ddUseExample('reminder')">
            🔔 My next reminder
        </button>

        <button onclick="ddUseExample('medicine')">
            💊 My medicine
        </button>

        <button onclick="ddUseExample('game')">
            🧠 Start a game
        </button>

    </div>

</section>


<style>

.dd-voice-card {

    margin: 30px 0;

    padding: 32px;

    border-radius: 28px;

    background:
        linear-gradient(
            135deg,
            #fff8ed,
            #f4f8ef
        );

    border: 1px solid #eadfce;

    box-shadow:
        0 15px 40px rgba(
            73,
            65,
            50,
            0.08
        );

}


.dd-voice-header {

    display: flex;

    justify-content: space-between;

    gap: 25px;

    align-items: flex-start;

}


.dd-voice-label {

    color: #d97745;

    font-size: 12px;

    font-weight: 800;

    letter-spacing: 2px;

}


.dd-voice-card h2 {

    margin: 8px 0;

    color: #24483b;

}


.dd-voice-card p {

    color: #68756f;

    margin: 0;

}


.dd-language-box {

    display: flex;

    flex-direction: column;

    gap: 7px;

}


.dd-language-box label {

    font-size: 13px;

    font-weight: 700;

    color: #526158;

}


.dd-language-box select {

    border: 1px solid #d9cfbf;

    background: white;

    padding: 11px 15px;

    border-radius: 12px;

    font-size: 14px;

    cursor: pointer;

}


.dd-voice-center {

    text-align: center;

    padding: 30px 10px 20px;

}


.dd-mic-button {

    width: 100px;

    height: 100px;

    border-radius: 50%;

    border: none;

    background: #e78b55;

    color: white;

    font-size: 40px;

    cursor: pointer;

    box-shadow:
        0 10px 30px rgba(
            231,
            139,
            85,
            0.30
        );

    transition: 0.25s;

}


.dd-mic-button:hover {

    transform: scale(1.06);

}


.dd-mic-button.listening {

    animation: ddPulse 1.2s infinite;

}


@keyframes ddPulse {

    0% {
        box-shadow:
            0 0 0 0 rgba(
                231,
                139,
                85,
                0.45
            );
    }

    70% {
        box-shadow:
            0 0 0 25px rgba(
                231,
                139,
                85,
                0
            );
    }

    100% {
        box-shadow:
            0 0 0 0 rgba(
                231,
                139,
                85,
                0
            );
    }

}


.dd-voice-status {

    margin-top: 18px;

    color: #65716b;

    font-weight: 600;

}


.dd-voice-text {

    margin-top: 12px;

    font-size: 17px;

    color: #24483b;

    min-height: 25px;

}


.dd-voice-response {

    margin: 18px auto 0;

    max-width: 600px;

    padding: 14px 18px;

    border-radius: 15px;

    background: white;

    color: #24483b;

    display: none;

}


.dd-voice-examples {

    display: flex;

    flex-wrap: wrap;

    align-items: center;

    justify-content: center;

    gap: 10px;

}


.dd-voice-examples span {

    color: #7b827d;

    font-size: 13px;

}


.dd-voice-examples button {

    border: 1px solid #ded5c7;

    background: white;

    padding: 10px 14px;

    border-radius: 12px;

    cursor: pointer;

}


@media (max-width: 700px) {

    .dd-voice-header {

        flex-direction: column;

    }

    .dd-language-box {

        width: 100%;

    }

    .dd-language-box select {

        width: 100%;

    }

}

</style>


<script>

let ddRecognition = null;

let ddLanguage = "en";

const ddPatientId = "{{ patient_id }}";


function ddChangeLanguage(language) {

    ddLanguage = language;

    if (ddRecognition) {

        ddRecognition.lang =
            ddGetSpeechCode(language);

    }

}


function ddGetSpeechCode(language) {

    const languages = {

        en: "en-IN",

        hi: "hi-IN",

        mr: "mr-IN"

    };

    return languages[language] || "en-IN";

}


function ddGetText(key) {

    const text = {

        en: {
            listening: "Listening...",
            speak: "Tap the microphone and speak",
            unsupported: "Voice recognition is not supported in this browser.",
            error: "Sorry, I could not understand that."
        },

        hi: {
            listening: "मैं सुन रहा हूँ...",
            speak: "माइक्रोफोन दबाकर बोलें",
            unsupported: "इस ब्राउज़र में वॉइस सुविधा उपलब्ध नहीं है।",
            error: "माफ़ कीजिए, मैं समझ नहीं पाया।"
        },

        mr: {
            listening: "मी ऐकत आहे...",
            speak: "मायक्रोफोन दाबून बोला",
            unsupported: "या ब्राउझरमध्ये व्हॉइस सुविधा उपलब्ध नाही.",
            error: "माफ करा, मला समजले नाही."
        }

    };

    return text[ddLanguage][key];

}


function ddCreateRecognition() {

    const SpeechRecognition =
        window.SpeechRecognition ||
        window.webkitSpeechRecognition;


    if (!SpeechRecognition) {

        return null;

    }


    const recognition =
        new SpeechRecognition();


    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.lang =
        ddGetSpeechCode(ddLanguage);


    recognition.onstart = function () {

        const button =
            document.getElementById(
                "ddVoiceButton"
            );

        button.classList.add(
            "listening"
        );

        document.getElementById(
            "ddVoiceStatus"
        ).innerText =
            ddGetText("listening");

    };


    recognition.onresult = function(event) {

        const command =
            event.results[0][0].transcript;


        document.getElementById(
            "ddVoiceText"
        ).innerText =
            "“" + command + "”";


        ddSendCommand(command);

    };


    recognition.onerror = function(event) {

        console.log(
            "Voice error:",
            event.error
        );


        document.getElementById(
            "ddVoiceStatus"
        ).innerText =
            ddGetText("error");


        ddResetMic();

    };


    recognition.onend = function() {

        ddResetMic();

    };


    return recognition;

}


function ddStartListening() {

    if (!ddRecognition) {

        ddRecognition =
            ddCreateRecognition();

    }


    if (!ddRecognition) {

        alert(
            ddGetText("unsupported")
        );

        return;

    }


    ddRecognition.lang =
        ddGetSpeechCode(ddLanguage);


    document.getElementById(
        "ddVoiceResponse"
    ).style.display = "none";


    try {

        ddRecognition.start();

    } catch(error) {

        console.log(error);

    }

}


function ddResetMic() {

    const button =
        document.getElementById(
            "ddVoiceButton"
        );

    button.classList.remove(
        "listening"
    );


    document.getElementById(
        "ddVoiceStatus"
    ).innerText =
        ddGetText("speak");

}


async function ddSendCommand(command) {

    try {

        const response =
            await fetch(
                "/ai/voice/command/",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({

                        command: command,

                        patient_id:
                            ddPatientId,

                        language:
                            ddLanguage

                    })

                }
            );


        const data =
            await response.json();


        if (!data.success) {

            throw new Error(
                data.error ||
                "Something went wrong."
            );

        }


        const responseBox =
            document.getElementById(
                "ddVoiceResponse"
            );


        responseBox.innerText =
            "🔊 " + data.response;


        responseBox.style.display =
            "block";


        ddSpeak(data.response);


        if (data.redirect) {

            setTimeout(
                function() {

                    window.location.href =
                        data.redirect;

                },
                1800
            );

        }


    } catch(error) {

        console.error(error);

        document.getElementById(
            "ddVoiceResponse"
        ).innerText =
            "⚠️ " + error.message;

        document.getElementById(
            "ddVoiceResponse"
        ).style.display =
            "block";

    }

}


function ddSpeak(text) {

    if (!("speechSynthesis" in window)) {

        return;

    }


    window.speechSynthesis.cancel();


    const speech =
        new SpeechSynthesisUtterance(
            text
        );


    speech.lang =
        ddGetSpeechCode(ddLanguage);


    speech.rate = 0.85;

    speech.pitch = 1;


    window.speechSynthesis.speak(
        speech
    );

}


function ddUseExample(type) {

    const examples = {

        en: {
            reminder: "My next reminder",
            medicine: "My medicine",
            game: "Start a game"
        },

        hi: {
            reminder: "मेरी अगली रिमाइंडर",
            medicine: "मेरी दवाई",
            game: "गेम शुरू करो"
        },

        mr: {
            reminder: "माझी पुढची आठवण",
            medicine: "माझी औषधे",
            game: "गेम सुरू करा"
        }

    };


    const command =
        examples[ddLanguage][type];


    document.getElementById(
        "ddVoiceText"
    ).innerText =
        "“" + command + "”";


    ddSendCommand(command);

}

</script>

{% endif %}
'''

(
    BASE_DIR /
    "ai_engine" /
    "templates" /
    "ai_engine" /
    "voice_assistant.html"
).write_text(
    voice_html,
    encoding="utf-8"
)


# ============================================================
# 10. ADD VOICE ASSISTANT TO PATIENT DASHBOARD
# ============================================================

dashboard = (
    BASE_DIR /
    "patients" /
    "templates" /
    "patients" /
    "patient_dashboard.html"
)

if dashboard.exists():

    content = dashboard.read_text(
        encoding="utf-8"
    )

    include_code = (
        '{% include "ai_engine/voice_assistant.html" '
        'with patient_id=patient.id %}'
    )

    if "ai_engine/voice_assistant.html" not in content:

        if "</body>" in content:

            content = content.replace(
                "</body>",
                include_code + "\n\n</body>"
            )

        else:

            content += "\n\n" + include_code

        dashboard.write_text(
            content,
            encoding="utf-8"
        )

        print(
            "Voice assistant added to patient dashboard."
        )

    else:

        print(
            "Voice assistant already exists in dashboard."
        )

else:

    print(
        "WARNING: Patient dashboard template was not found."
    )


print()
print("=" * 60)
print("DONGDAWN VOICE + MULTILINGUAL SETUP COMPLETE")
print("=" * 60)
print()
print("Created:")
print("  ai_engine/services/")
print("  ai_engine/voice/")
print("  ai_engine/templates/ai_engine/voice_assistant.html")
print()
print("Languages:")
print("  English")
print("  Hindi")
print("  Marathi")
print()
print("Voice:")
print("  Speech Recognition")
print("  Text-to-Speech")
print()
print("Voice commands:")
print("  Reminders")
print("  Medicine")
print("  Cognitive Games")
print()
print("Next: run python manage.py check")