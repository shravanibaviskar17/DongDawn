from deep_translator import GoogleTranslator


LANGUAGES = {
    "en": {
        "name": "English",
        "code": "en",
    },
    "hi": {
        "name": "Hindi",
        "code": "hi",
    },
    "mr": {
        "name": "Marathi",
        "code": "mr",
    },
    "as": {
        "name": "Assamese",
        "code": "as",
    },
    "bn": {
        "name": "Bengali",
        "code": "bn",
    },
    "mni": {
        "name": "Manipuri",
        "code": "mni",
    },
    "ne": {
        "name": "Nepali",
        "code": "ne",
    },
    "brx": {
        "name": "Bodo",
        "code": "brx",
    },
    "kha": {
        "name": "Khasi",
        "code": "kha",
    },
    "lus": {
        "name": "Mizo",
        "code": "lus",
    },
    "kok": {
        "name": "Kokborok",
        "code": "kok",
    },
}


TRANSLATIONS = {

    "medicine": {
        "en": "Medicine reminder",
        "hi": "दवाई की याद",
        "mr": "औषधांची आठवण",
        "as": "ঔষধৰ সোঁৱৰণী",
        "bn": "ওষুধের রিমাইন্ডার",
        "mni": "ꯑꯣꯁꯨꯗꯒꯤ ꯅꯤꯡꯊꯤꯅꯕ",
        "ne": "औषधिको सम्झना",
        "brx": "दावाइनि सानखांथि",
        "kha": "Ka jingkynmaw dawai",
        "lus": "Damdawi hriat rengna",
        "kok": "Davaichi mhozo hriat",
    },

    "game": {
        "en": "Let's start a cognitive game.",
        "hi": "आइए एक संज्ञानात्मक गेम शुरू करते हैं।",
        "mr": "चला एक संज्ञानात्मक गेम सुरू करूया.",
        "as": "আহক এটা জ্ঞানমূলক খেল আৰম্ভ কৰোঁ।",
        "bn": "চলুন একটি জ্ঞানীয় খেলা শুরু করি।",
        "mni": "ꯑꯍꯥꯟꯕ ꯀꯣꯒꯅꯤꯇꯤꯚ ꯒꯦꯝ ꯍꯧꯖꯤꯜꯂꯨꯁꯤ।",
        "ne": "एउटा संज्ञानात्मक खेल सुरु गरौँ।",
        "brx": "आं सोलोंनाय गेम जागायगोन।",
        "kha": "To ngin sdang ïa ka cognitive game.",
        "lus": "Cognitive game pakhat tan ila.",
        "kok": "Ek cognitive game suru koruya.",
    },

    "unknown": {
        "en": "Sorry, I did not understand your request.",
        "hi": "माफ़ कीजिए, मैं आपकी बात समझ नहीं पाया।",
        "mr": "माफ करा, मला तुमचे म्हणणे समजले नाही.",
        "as": "ক্ষমা কৰিব, মই আপোনাৰ কথাটো বুজিব নোৱাৰিলোঁ।",
        "bn": "দুঃখিত, আমি আপনার কথা বুঝতে পারিনি।",
        "mni": "ꯃꯥꯐꯝ, ꯑꯩꯅ ꯅꯍꯥꯛꯀꯤ ꯋꯥꯐꯝ ꯈꯪꯗꯦ।",
        "ne": "माफ गर्नुहोस्, मैले तपाईंको कुरा बुझिनँ।",
        "brx": "माफ खालाम, आं नोंनि बुंनायखौ बुजिनो हायाखै।",
        "kha": "Map, ngam sngewthuh ïa ka jingkren jong phi.",
        "lus": "Ka ngaihdam, ka thu sawi hi ka hre lo.",
        "kok": "Maf kor, mhaka tumchi magom somzunk zaina.",
    },

}


def get_language(language):
    """
    Return a supported language code.
    """

    if not language:
        return "en"

    language = language.lower().strip()

    if language in LANGUAGES:
        return language

    return "en"


def get_translation(key, language="en"):
    """
    Return translated text for the selected language.
    """

    language = get_language(language)

    if key in TRANSLATIONS:
        return TRANSLATIONS[key].get(
            language,
            TRANSLATIONS[key]["en"]
        )

    return ""


def translate_text(text, target_language="en"):
    """
    Translate text using GoogleTranslator.
    """

    target_language = get_language(target_language)

    if target_language == "en":
        return text

    try:
        translated = GoogleTranslator(
            source="auto",
            target=LANGUAGES[target_language]["code"]
        ).translate(text)

        return translated

    except Exception as error:

        print(
            "Translation error:",
            error
        )

        return text