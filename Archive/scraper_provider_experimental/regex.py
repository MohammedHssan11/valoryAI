import re

PHONE_RE = re.compile(r'(\+?\d[\d\s\-\(\)]{8,}\d)')
WHATS_RE = re.compile(r'whatsapp', re.I)

def sanitize_description(text: str | None) -> str | None:
    if not text:
        return text
    # remove phone-like patterns
    t = PHONE_RE.sub("[PHONE]", text)
    # normalize whatsapp mentions
    t = WHATS_RE.sub("WhatsApp", t)
    return t
