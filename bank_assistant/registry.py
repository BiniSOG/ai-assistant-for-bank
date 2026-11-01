"""Mock National ID (Fayda) registry and OTP service.

Replace ``lookup_identity`` with the real Fayda eKYC API and ``send_otp`` with
your SMS gateway to go to production.
"""
from __future__ import annotations

import hashlib
import hmac
import secrets
import time

from . import config
from .state import IdentityRecord, OnboardingState

# Sample records for testing. Any other 12-digit FAN is "found" using the details
# the customer gave the assistant, so every tester can complete the flow.
SAMPLE_RECORDS: dict[str, IdentityRecord] = {
    "123456789012": IdentityRecord(
        full_name="Betelhem Tesfaye Alemu",
        date_of_birth="2000-01-15",
        birth_city="Addis Ababa",
        nationality="Ethiopian",
        phone="+251911231234",
    ),
    "987654321098": IdentityRecord(
        full_name="Abebe Kebede Bekele",
        date_of_birth="1992-06-03",
        birth_city="Bahir Dar",
        nationality="Ethiopian",
        phone="+251922345678",
    ),
}


def _phone_for(fan: str) -> str:
    h = int(hashlib.sha256(fan.encode()).hexdigest(), 16)
    return f"+2519{h % 10**8:08d}"


def lookup_identity(fan: str, state: OnboardingState) -> IdentityRecord:
    if fan in SAMPLE_RECORDS:
        return SAMPLE_RECORDS[fan]
    return IdentityRecord(
        full_name=state.full_name or "Customer",
        date_of_birth=state.date_of_birth or "2000-01-01",
        birth_city=state.birth_city or "Addis Ababa",
        nationality=state.nationality or "Ethiopian",
        phone=_phone_for(fan),
    )


def mask_phone(phone: str) -> str:
    return f"{phone[:5]} ** *** {phone[-4:]}"


def _otp_hash(fan: str, code: str, expires: int) -> str:
    msg = f"{fan}:{code}:{expires}".encode()
    return hmac.new(config.APP_SECRET.encode(), msg, hashlib.sha256).hexdigest()


def send_otp(state: OnboardingState) -> str:
    """Generate an OTP, store its hash in the state and 'send' it. Returns the code."""
    assert state.fan
    code = f"{secrets.randbelow(10**6):06d}"
    expires = int(time.time()) + config.OTP_TTL_SECONDS
    state.otp_hash = _otp_hash(state.fan, code, expires)
    state.otp_expires = expires
    state.otp_attempts = 0
    # TODO: integrate SMS gateway here, e.g. sms.send(identity.phone, f"Dashen Bank OTP: {code}")
    return code


def check_otp(state: OnboardingState, code: str) -> str:
    """Returns 'ok', 'bad', 'expired' or 'locked'."""
    if not state.otp_hash or not state.otp_expires or not state.fan:
        return "expired"
    if state.otp_attempts >= config.OTP_MAX_ATTEMPTS:
        return "locked"
    if time.time() > state.otp_expires:
        return "expired"
    state.otp_attempts += 1
    if hmac.compare_digest(_otp_hash(state.fan, code, state.otp_expires), state.otp_hash):
        return "ok"
    return "locked" if state.otp_attempts >= config.OTP_MAX_ATTEMPTS else "bad"
