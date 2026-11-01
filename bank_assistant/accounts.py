"""Mock core-banking account creation."""
from __future__ import annotations

import hashlib

from . import config
from .state import OnboardingState


def create_account(state: OnboardingState) -> str:
    """Return a deterministic 12-digit account number (idempotent per FAN + type)."""
    seed = f"{config.APP_SECRET}:{state.fan}:{state.account_type}".encode()
    n = int(hashlib.sha256(seed).hexdigest(), 16) % 10**8
    return f"1000{n:08d}"


def format_account_number(number: str) -> str:
    return f"{number[:4]} {number[4:8]} {number[8:]}"
