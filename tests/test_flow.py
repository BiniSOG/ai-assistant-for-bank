from datetime import date

import pytest
from fastapi.testclient import TestClient

from api.index import app
from bank_assistant import validators as v

client = TestClient(app)


def post(path, body):
    r = client.post(path, json=body)
    assert r.status_code == 200, r.text
    return r.json()


def say(res, message):
    return post("/api/chat", {"state": res["state"], "token": res["token"], "message": message})


def test_full_flow_sample_fan():
    res = post("/api/session/start", {"lang": "en"})
    assert "Welcome to Dashen Bank" in res["reply"]
    res = say(res, "Yes, let's start")
    assert res["view"]["step"] == "full_name"
    res = say(res, "My name is Betelhem Tesfaye Alemu")
    assert res["view"]["full_name"] == "Betelhem Tesfaye Alemu"
    res = say(res, "Jan 15, 2000")
    assert res["view"]["date_of_birth"] == "2000-01-15"
    res = say(res, "I was born in addis abeba")
    assert res["view"]["birth_city"] == "Addis Ababa"
    res = say(res, "Ethiopian")
    res = say(res, "savings please")
    assert res["view"]["account_type"] == "Savings Account"
    res = say(res, "1234 5678 9012")
    assert res["view"]["step"] == "otp"
    code = res["extra"]["demo_otp"]

    bad = post("/api/otp/verify", {"state": res["state"], "token": res["token"], "code": "000000" if code != "000000" else "111111"})
    assert bad["view"]["step"] == "otp"

    res = post("/api/otp/verify", {"state": res["state"], "token": res["token"], "code": code})
    assert res["view"]["step"] == "review"
    assert res["view"]["identity"]["full_name"] == "Betelhem Tesfaye Alemu"
    assert res["view"]["mismatches"] == []

    res = post("/api/review", {"state": res["state"], "token": res["token"], "action": "confirm"})
    res = post("/api/account/create", {"state": res["state"], "token": res["token"]})
    assert res["view"]["step"] == "done"
    assert res["extra"]["account_number"].startswith("1000 ")


def test_tampered_state_rejected():
    res = post("/api/session/start", {"lang": "en"})
    state = dict(res["state"], step="creating", verified=True)
    r = client.post("/api/account/create", json={"state": state, "token": res["token"]})
    assert r.status_code == 400


def test_invalid_answers_reprompt():
    res = post("/api/session/start", {"lang": "am"})
    res = say(res, "አዎ")
    assert res["view"]["step"] == "full_name"
    res = say(res, "x")
    assert res["view"]["step"] == "full_name"


@pytest.mark.parametrize(
    "text,expected",
    [
        ("Jan 15, 2000", "2000-01-15"),
        ("15 January 2000", "2000-01-15"),
        ("15/01/2000", "2000-01-15"),
        ("2000-01-15", "2000-01-15"),
        ("January 15th, 2000", "2000-01-15"),
    ],
)
def test_parse_dates(text, expected):
    assert v.parse_date_of_birth(text, today=date(2026, 1, 1)).value == expected


def test_underage():
    assert v.parse_date_of_birth("2015-01-01", today=date(2026, 1, 1)).error == "err_underage"


def test_fan_spoken():
    assert v.parse_fan("one two three four five six seven eight nine zero one two").value == "123456789012"
    assert not v.parse_fan("12345").ok


LANGS = ["en", "am", "om", "ti", "so", "aa"]


def test_every_language_has_every_message():
    from bank_assistant.messages import ACKS, LANGUAGES, MESSAGES

    assert set(MESSAGES) == set(LANGUAGES) == set(ACKS) == set(LANGS)
    for lang, table in MESSAGES.items():
        assert set(table) == set(MESSAGES["en"]), lang


@pytest.mark.parametrize(
    "lang,yes,name,city,nationality,account",
    [
        ("om", "Eeyyee", "Maqaan koo Caalaa Tolaa Gammachuu dha", "Finfinnee", "Itoophiyaa", "Qusannaa"),
        ("ti", "እወ", "ስመይ ሃብቶም ገብረመድህን ተስፋይ እዩ", "መቐለ", "ኢትዮጵያዊ", "ቁጠባ"),
        ("so", "Haa", "Magacaygu waa Cabdi Maxamed Cali", "Waxaan ku dhashay Jigjiga", "Itoobiyaan", "Kaydin"),
        ("aa", "Ey", "Yi migaq Ali Mohammed Ahmed", "Samara", "Ethiopian", "Savings"),
    ],
)
def test_flow_in_new_languages(lang, yes, name, city, nationality, account):
    from bank_assistant.messages import MESSAGES

    res = post("/api/session/start", {"lang": lang})
    assert res["reply"] == MESSAGES[lang]["greeting"]
    res = say(res, yes)
    assert res["view"]["step"] == "full_name"
    for answer in (name, "1995-03-20", city, nationality, account):
        res = say(res, answer)
    v = res["view"]
    assert v["step"] == "fan", res["reply"]
    assert v["account_type"] == "Savings Account"
    assert v["nationality"] == "Ethiopian"
    res = say(res, "9999 8888 7777")
    assert res["view"]["step"] == "otp"
    assert "{phone}" not in res["reply"] and res["extra"]["phone"] in res["reply"]


def test_unknown_language_rejected():
    assert client.post("/api/session/start", json={"lang": "xx"}).status_code == 422
