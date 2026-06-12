from __future__ import annotations

import re
import unicodedata


ARABIC_DIACRITICS_RE = re.compile(r"[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED]")
PUNCTUATION_RE = re.compile(r"[\u0000-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u007E\u060C\u061B\u061F\u066A-\u066D]+")
WHITESPACE_RE = re.compile(r"\s+")

ARABIC_DIGITS = str.maketrans(
    {
        "٠": "0",
        "١": "1",
        "٢": "2",
        "٣": "3",
        "٤": "4",
        "٥": "5",
        "٦": "6",
        "٧": "7",
        "٨": "8",
        "٩": "9",
        "۰": "0",
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
    }
)

ARABIC_LETTER_FOLDING = str.maketrans(
    {
        "\u0640": "",
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ٱ": "ا",
        "ى": "ي",
        "ئ": "ي",
        "ؤ": "و",
        "ة": "ه",
    }
)

TOKEN_SYNONYMS = {
    "el": "al",
    "alsheikh": "sheikh",
    "elshiekh": "sheikh",
    "elsheikh": "sheikh",
    "shiekh": "sheikh",
    "shaikh": "sheikh",
    "settlement": "tagamoa",
    "tagamo": "tagamoa",
    "tagamo3": "tagamoa",
    "tgamo3": "tagamoa",
    "tgamoo3": "tagamoa",
    "oct": "october",
    "oktober": "october",
    "oktobar": "october",
    "rehab": "rehab",
}

CANONICAL_EQUIVALENTS = {
    "مدينتي": "مدينتي",
    "madinaty": "مدينتي",
    "madinty": "مدينتي",
    "madenaty": "مدينتي",
    "madenity": "مدينتي",
    "الرحاب": "الرحاب",
    "rehab": "الرحاب",
    "al rehab": "الرحاب",
    "el rehab": "الرحاب",
    "sheikh zayed": "الشيخ زايد",
    "zayed": "الشيخ زايد",
    "الشيخ زايد": "الشيخ زايد",
    "6 october": "السادس من اكتوبر",
    "6th october": "السادس من اكتوبر",
    "sixth october": "السادس من اكتوبر",
    "october": "السادس من اكتوبر",
    "اكتوبر": "السادس من اكتوبر",
    "السادس من اكتوبر": "السادس من اكتوبر",
    "new cairo": "القاهره الجديده",
    "القاهره الجديده": "القاهره الجديده",
    "tagamoa": "التجمع الخامس",
    "fifth tagamoa": "التجمع الخامس",
    "fifth settlement": "التجمع الخامس",
    "5th settlement": "التجمع الخامس",
    "5th tagamoa": "التجمع الخامس",
    "التجمع الخامس": "التجمع الخامس",
    "new capital": "العاصمه الاداريه الجديده",
    "nac": "العاصمه الاداريه الجديده",
    "العاصمه الاداريه": "العاصمه الاداريه الجديده",
    "العاصمه الاداريه الجديده": "العاصمه الاداريه الجديده",
}

STOP_WORDS = {
    "the", "city", "district", "compound", "compounds", "governorate"
}


def normalize_address_text(value: str | None) -> str:
    if value is None:
        return ""

    text = unicodedata.normalize("NFKC", str(value))
    text = text.translate(ARABIC_DIGITS)
    text = ARABIC_DIACRITICS_RE.sub("", text)
    text = text.translate(ARABIC_LETTER_FOLDING)
    text = text.casefold()
    text = PUNCTUATION_RE.sub(" ", text)
    text = WHITESPACE_RE.sub(" ", text).strip()

    if not text:
        return ""

    tokens = []
    for token in text.split():
        if token in STOP_WORDS:
            continue
        tokens.append(TOKEN_SYNONYMS.get(token, token))
    return " ".join(tokens)


def canonical_location_key(value: str | None) -> str:
    normalized = normalize_address_text(value)
    if not normalized:
        return ""
    return CANONICAL_EQUIVALENTS.get(normalized, normalized)


def normalize_entity_type(value: str | None) -> str:
    return normalize_address_text(value).replace(" ", "_")
