"""Runtime configuration, read from environment variables."""
from __future__ import annotations

import os


def _bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


# Secret used to sign the conversation state and OTP hashes.
# ALWAYS set APP_SECRET in production (Vercel → Settings → Environment Variables).
APP_SECRET: str = os.getenv("APP_SECRET", "dev-only-insecure-secret-change-me")

# There is no SMS gateway in this demo, so by default the OTP is returned to the
# browser and shown in a "demo" banner. Set DEMO_SHOW_OTP=false once a real
# SMS provider is wired into registry.send_otp().
DEMO_SHOW_OTP: bool = _bool("DEMO_SHOW_OTP", True)

OTP_TTL_SECONDS: int = int(os.getenv("OTP_TTL_SECONDS", "300"))
OTP_MAX_ATTEMPTS: int = int(os.getenv("OTP_MAX_ATTEMPTS", "5"))
MIN_AGE: int = int(os.getenv("MIN_AGE", "18"))

# LLM selection. LLM_PROVIDER = auto | anthropic | openai | none
LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "auto").strip().lower()
LLM_MODEL: str | None = os.getenv("LLM_MODEL") or None
LLM_TIMEOUT: float = float(os.getenv("LLM_TIMEOUT", "15"))
