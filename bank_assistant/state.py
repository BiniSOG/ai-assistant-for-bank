"""Conversation state.

Vercel runs Python as stateless serverless functions, so the state travels with
the client. It is signed with HMAC so the browser cannot e.g. skip OTP
verification by editing ``step`` or ``verified``.
"""
from __future__ import annotations

import hashlib
import hmac
import json
from typing import Literal

from pydantic import BaseModel, Field

from . import config

Lang = Literal["en", "am", "om", "ti", "so", "aa"]

Step = Literal[
    "greeting",
    "full_name",
    "date_of_birth",
    "birth_city",
    "nationality",
    "account_type",
    "fan",
    "otp",
    "review",
    "creating",
    "done",
]

QUESTION_STEPS: tuple[str, ...] = (
    "full_name",
    "date_of_birth",
    "birth_city",
    "nationality",
    "account_type",
    "fan",
)


class IdentityRecord(BaseModel):
    """A record as returned by the (mock) National ID / Fayda registry."""

    full_name: str
    date_of_birth: str
    birth_city: str
    nationality: str
    phone: str


class OnboardingState(BaseModel):
    step: Step = "greeting"
    lang: Lang = "en"

    full_name: str | None = None
    date_of_birth: str | None = None
    birth_city: str | None = None
    nationality: str | None = None
    account_type: str | None = None
    fan: str | None = None

    otp_hash: str | None = None
    otp_expires: int | None = None
    otp_attempts: int = 0
    verified: bool = False
    identity: IdentityRecord | None = None
    mismatches: list[str] = Field(default_factory=list)

    account_number: str | None = None


class InvalidState(Exception):
    pass


def _canonical(state: OnboardingState) -> bytes:
    return json.dumps(state.model_dump(mode="json"), sort_keys=True, separators=(",", ":")).encode()


def sign(state: OnboardingState) -> str:
    return hmac.new(config.APP_SECRET.encode(), _canonical(state), hashlib.sha256).hexdigest()


def load(raw: dict | None, token: str | None) -> OnboardingState:
    if not raw:
        raise InvalidState("missing state")
    state = OnboardingState.model_validate(raw)
    if not token or not hmac.compare_digest(sign(state), token):
        raise InvalidState("bad signature")
    return state
