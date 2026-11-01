"""Deterministic parsing / validation of customer answers.

These run on every answer – whether the LLM extracted the value or not – so the
data that reaches the core banking step is always normalised and validated in
plain Python.
"""
from __future__ import annotations

import difflib
import re
from dataclasses import dataclass
from datetime import date

from . import config

ETHIOPIC = r"ሀ-፿"
_ETHIOPIC_RE = re.compile(f"[{ETHIOPIC}]")


def has_ethiopic(text: str) -> bool:
    return bool(_ETHIOPIC_RE.search(text or ""))


@dataclass
class Parsed:
    ok: bool
    value: str | None = None
    error: str | None = None  # message key in messages.py


# --------------------------------------------------------------------------- yes / no
_AFFIRM = {
    "yes", "yeah", "yep", "yup", "sure", "ok", "okay", "start", "go", "ready",
    "let's", "lets", "please", "of course", "absolutely", "alright", "fine",
    "አዎ", "እሺ", "አዎን", "ጀምር", "እንጀምር",                       # Amharic
    "eeyyee", "eeyye", "eeyyeen", "tole", "jalqabnu",              # Afaan Oromo
    "እወ", "ሕራይ", "ንጀምር",                                       # Tigrinya
    "haa", "haye", "waayahay", "bilowno", "bilaabno",              # Somali
    "ey", "qimbisna", "qimbisnay",                                 # Afar
}
_DENY = {
    "no", "nope", "not now", "later", "stop", "cancel",
    "አይ", "አልፈልግም", "አይደለም",                                   # Amharic
    "lakki", "hin barbaadu",                                       # Afaan Oromo
    "ኣይፋል", "ኣይደልን", "ኣይፋልን",                                 # Tigrinya
    "maya", "hadda maya",                                          # Somali
    "hinna", "maleh",                                              # Afar
}


def yes_no(text: str) -> str | None:
    t = (text or "").strip().lower()
    words = set(re.findall(rf"[a-z']+|[{ETHIOPIC}]+", t))
    phrases = [p for p in _DENY if " " in p]
    if any(p in t for p in ("not now", "no thanks", "no thank", *phrases)) or words & _DENY:
        return "deny"
    if words & _AFFIRM or any(p in t for p in ("let's go", "of course", "get started")):
        return "affirm"
    return None


# --------------------------------------------------------------------------- full name
_NAME_PREFIXES = re.compile(
    r"^(?:hi|hello|hey|selam|ሰላም)?[,!. ]*"
    r"(?:my (?:full )?name is|my name's|i am|i'm|im|it is|it's|this is|call me|name|ስሜ|ሙሉ ስሜ"
    r"|maqaan (?:koo|kiyya)(?: guutuun)?|ani"          # Afaan Oromo
    r"|ስመይ|ምሉእ ስመይ"                                   # Tigrinya
    r"|magacayg(?:u|a)(?: oo buuxa)?(?: waa)?|waxaan ahay|waa"  # Somali
    r"|yi migaq(?: inkih)?)"                            # Afar
    r"(?=[\s:,]|$)[\s:,]*",  # whole words only, so "Imran" / "Anissa" are not trimmed
    re.IGNORECASE,
)


def parse_full_name(text: str) -> Parsed:
    t = (text or "").strip()
    t = _NAME_PREFIXES.sub("", t).strip()
    t = re.sub(r"\s+(?:ነው|ይባላል|እዩ|ይበሃል|dha|jedhama|kinni)[.!።]*$", "", t)
    t = re.sub(r"[.!?,።]+$", "", t).strip()
    t = re.sub(r"\s+", " ", t)
    if not re.fullmatch(rf"[A-Za-z{ETHIOPIC}'\-. ]+", t or "-"):
        return Parsed(False, error="err_name")
    parts = [p for p in t.split(" ") if p]
    if len(parts) < 2 or any(len(p) < 2 for p in parts) or len(t) > 80:
        return Parsed(False, error="err_name")
    if not has_ethiopic(t):
        t = " ".join(p[:1].upper() + p[1:].lower() for p in parts)
    return Parsed(True, t)


# --------------------------------------------------------------------------- date of birth
_MONTHS = {
    m: i
    for i, names in enumerate(
        [
            ("january", "jan"), ("february", "feb"), ("march", "mar"), ("april", "apr"),
            ("may",), ("june", "jun"), ("july", "jul"), ("august", "aug"),
            ("september", "sep", "sept"), ("october", "oct"), ("november", "nov"),
            ("december", "dec"),
        ],
        start=1,
    )
    for m in names
}
_MONTH_RE = "|".join(sorted(_MONTHS, key=len, reverse=True))


def _safe_date(y: int, m: int, d: int) -> date | None:
    try:
        return date(y, m, d)
    except ValueError:
        return None


def parse_date(text: str) -> date | None:
    t = (text or "").strip().lower()
    t = re.sub(r"(\d)(st|nd|rd|th)\b", r"\1", t)
    if m := re.search(r"\b(\d{4})[-/. ](\d{1,2})[-/. ](\d{1,2})\b", t):
        return _safe_date(int(m[1]), int(m[2]), int(m[3]))
    if m := re.search(r"\b(\d{1,2})[-/. ](\d{1,2})[-/. ](\d{4})\b", t):
        a, b, y = int(m[1]), int(m[2]), int(m[3])
        # Day-first (Ethiopian / international convention) unless impossible.
        if b > 12 and a <= 12:
            return _safe_date(y, a, b)
        return _safe_date(y, b, a)
    if m := re.search(rf"\b({_MONTH_RE})\.?\s+(\d{{1,2}}),?\s+(\d{{4}})\b", t):
        return _safe_date(int(m[3]), _MONTHS[m[1]], int(m[2]))
    if m := re.search(rf"\b(\d{{1,2}})\s+(?:of\s+)?({_MONTH_RE})\.?,?\s+(\d{{4}})\b", t):
        return _safe_date(int(m[3]), _MONTHS[m[2]], int(m[1]))
    return None


def age_on(born: date, today: date | None = None) -> int:
    today = today or date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def parse_date_of_birth(text: str, today: date | None = None) -> Parsed:
    born = parse_date(text)
    if not born:
        return Parsed(False, error="err_dob")
    age = age_on(born, today)
    if age < 0 or age > 120:
        return Parsed(False, error="err_dob")
    if age < config.MIN_AGE:
        return Parsed(False, error="err_underage")
    return Parsed(True, born.isoformat())


# --------------------------------------------------------------------------- city
ETHIOPIAN_CITIES = [
    "Addis Ababa", "Dire Dawa", "Bahir Dar", "Gondar", "Mekelle", "Hawassa", "Adama",
    "Jimma", "Dessie", "Harar", "Jijiga", "Shashemene", "Bishoftu", "Debre Markos",
    "Debre Birhan", "Arba Minch", "Hosaena", "Nekemte", "Asosa", "Gambela", "Semera",
    "Wolaita Sodo", "Dilla", "Kombolcha", "Axum", "Lalibela", "Debre Tabor", "Woldia",
    "Ambo", "Adigrat", "Bale Robe", "Gode", "Assela", "Batu", "Burayu",
]
_CITY_ALIASES = {
    "addis": "Addis Ababa", "addis abeba": "Addis Ababa", "finfinne": "Addis Ababa",
    "አዲስ አበባ": "Addis Ababa", "ድሬ ዳዋ": "Dire Dawa", "ድሬዳዋ": "Dire Dawa",
    "ባህር ዳር": "Bahir Dar", "ጎንደር": "Gondar", "መቀሌ": "Mekelle", "ሀዋሳ": "Hawassa",
    "አዳማ": "Adama", "ናዝሬት": "Adama", "nazret": "Adama", "awassa": "Hawassa",
    "ጅማ": "Jimma", "ደሴ": "Dessie", "ሐረር": "Harar", "debre zeit": "Bishoftu",
    # Afaan Oromo
    "finfinnee": "Addis Ababa", "adaamaa": "Adama", "jimmaa": "Jimma", "hawaasaa": "Hawassa",
    "bishooftuu": "Bishoftu", "naqamtee": "Nekemte", "amboo": "Ambo", "harar": "Harar",
    "dirree dawaa": "Dire Dawa", "shaashamannee": "Shashemene", "asallaa": "Assela",
    # Tigrinya
    "መቐለ": "Mekelle", "ኣክሱም": "Axum", "ዓዲግራት": "Adigrat", "ኣዲስ ኣበባ": "Addis Ababa",
    "ሽረ": "Shire", "ዓድዋ": "Adwa",
    # Somali
    "jigjiga": "Jijiga", "diridhabe": "Dire Dawa", "diridhaba": "Dire Dawa", "godey": "Gode",
    "qabridahar": "Kebri Dahar", "dhagaxbuur": "Degehabur", "addis ababa": "Addis Ababa",
    # Afar
    "samara": "Semera", "asayta": "Asaita", "aysaqiita": "Asaita", "awsi": "Asaita",
}
_CITY_PREFIX = re.compile(
    r"^(?:i was born in|i was born at|born in|i'm from|i am from|from|in|it's|it is|the city is"
    r"|waxaan ku dhashay|magaalada)\s+",
    re.IGNORECASE,
)


def parse_city(text: str) -> Parsed:
    t = (text or "").strip()
    t = _CITY_PREFIX.sub("", t)
    t = re.sub(r"\s+(?:ነው|ተወለድኩ|እዩ|ተወሊደ|dha|tti dhaladhe|keessatti dhaladhe)[.!።]*$", "", t)
    t = re.sub(r"(?:city|ከተማ)$", "", t, flags=re.IGNORECASE)
    t = re.sub(r"[.!?,።]+$", "", t).strip()
    if not t or len(t) > 60 or not re.fullmatch(rf"[A-Za-z{ETHIOPIC}'\-. ]+", t):
        return Parsed(False, error="err_city")
    if alias := _CITY_ALIASES.get(t.lower()) or _CITY_ALIASES.get(t):
        return Parsed(True, alias)
    match = difflib.get_close_matches(t.title(), ETHIOPIAN_CITIES, n=1, cutoff=0.8)
    if match:
        return Parsed(True, match[0])
    return Parsed(True, t if has_ethiopic(t) else t.title())


# --------------------------------------------------------------------------- nationality
_NATIONALITIES = {
    "ethiopia": "Ethiopian", "ethiopian": "Ethiopian", "ኢትዮጵያ": "Ethiopian",
    "ኢትዮጵያዊ": "Ethiopian", "ኢትዮጵያዊት": "Ethiopian", "habesha": "Ethiopian",
    "kenya": "Kenyan", "kenyan": "Kenyan", "eritrea": "Eritrean", "eritrean": "Eritrean",
    "somalia": "Somali", "somali": "Somali", "djibouti": "Djiboutian",
    "sudan": "Sudanese", "sudanese": "Sudanese", "usa": "American",
    "united states": "American", "american": "American", "uk": "British",
    "british": "British", "united kingdom": "British",
    "itoophiyaa": "Ethiopian", "itiyoophiyaa": "Ethiopian", "itoophiyaawaa": "Ethiopian",
    "itoobiya": "Ethiopian", "itoobiyaan": "Ethiopian", "itiyoophiya": "Ethiopian",
    "ኤርትራ": "Eritrean", "ኤርትራዊ": "Eritrean", "ኤርትራዊት": "Eritrean",
    "soomaali": "Somali", "soomaaliya": "Somali", "jabuuti": "Djiboutian", "kenyaan": "Kenyan",
}


def parse_nationality(text: str) -> Parsed:
    t = re.sub(r"[.!?,።]+$", "", (text or "").strip()).strip()
    low = t.lower()
    for key, val in _NATIONALITIES.items():
        if re.search(rf"(?<![a-z]){re.escape(key)}(?![a-z])", low) or (has_ethiopic(key) and key in t):
            return Parsed(True, val)
    low = re.sub(r"^(?:i am|i'm|my nationality is|my country is|i'm from|i am from|from)\s+", "", low)
    if low and len(low) <= 40 and re.fullmatch(r"[a-z\- ]+", low):
        return Parsed(True, low.title())
    return Parsed(False, error="err_nationality")


# --------------------------------------------------------------------------- account type
ACCOUNT_TYPES = [
    "Savings Account",
    "Current Account",
    "Interest-Free (Wadiah) Savings",
    "Fixed Time Deposit",
]
_ACCOUNT_KEYWORDS = [
    (("interest free", "interest-free", "wadiah", "wadia", "islamic", "ከወለድ ነፃ", "ወለድ አልባ",
      "ብዘይ ወለድ", "dhala malee", "ribo la'aan", "ribo lahayn", "ribo"), 2),
    (("fixed", "time deposit", "term deposit", "ጊዜ ገደብ", "ግዜ ገደብ", "yeroo murtaa", "muddo go"), 3),
    (("current", "checking", "cheque", "check", "business", "ተንቀሳቃሽ", "ተንቀሳቓሲ",
      "deddeebii", "socda"), 1),
    (("saving", "savings", "save", "ቁጠባ", "qusannaa", "kaydin", "keydin", "qusba"), 0),
]


def parse_account_type(text: str) -> Parsed:
    low = (text or "").lower()
    for words, idx in _ACCOUNT_KEYWORDS:
        if any(w in low or w in (text or "") for w in words):
            return Parsed(True, ACCOUNT_TYPES[idx])
    for t in ACCOUNT_TYPES:
        if t.lower() == low.strip():
            return Parsed(True, t)
    return Parsed(False, error="err_account_type")


# --------------------------------------------------------------------------- FAN
_DIGIT_WORDS = {
    "zero": "0", "oh": "0", "o": "0", "one": "1", "two": "2", "to": "2", "too": "2",
    "three": "3", "four": "4", "for": "4", "five": "5", "six": "6", "seven": "7",
    "eight": "8", "nine": "9",
}


def digits_from_speech(text: str) -> str:
    out = []
    for tok in re.findall(r"[a-z]+|\d", (text or "").lower()):
        if tok.isdigit():
            out.append(tok)
        elif tok in _DIGIT_WORDS:
            out.append(_DIGIT_WORDS[tok])
        elif tok in ("double", "triple"):
            out.append(tok)
    # expand "double 5" / "triple 7"
    result: list[str] = []
    i = 0
    while i < len(out):
        if out[i] in ("double", "triple") and i + 1 < len(out) and out[i + 1].isdigit():
            result.append(out[i + 1] * (2 if out[i] == "double" else 3))
            i += 2
            continue
        if out[i].isdigit():
            result.append(out[i])
        i += 1
    return "".join(result)


def parse_fan(text: str) -> Parsed:
    digits = re.sub(r"\D", "", text or "")
    if len(digits) != 12:
        digits = digits_from_speech(text)
    if len(digits) != 12:
        return Parsed(False, error="err_fan")
    return Parsed(True, digits)


def format_fan(fan: str) -> str:
    return " ".join(fan[i : i + 4] for i in range(0, len(fan), 4))


def parse_otp(text: str) -> str | None:
    digits = re.sub(r"\D", "", text or "")
    return digits if len(digits) == 6 else None


PARSERS = {
    "full_name": parse_full_name,
    "date_of_birth": parse_date_of_birth,
    "birth_city": parse_city,
    "nationality": parse_nationality,
    "account_type": parse_account_type,
    "fan": parse_fan,
}
