"""Chat-model factory. Returns ``None`` when no provider is configured so the
agent can fall back to its deterministic rule-based interpreter."""
from __future__ import annotations

import logging
import os

from langchain_core.language_models.chat_models import BaseChatModel

from . import config

log = logging.getLogger(__name__)

DEFAULT_MODELS = {
    "anthropic": "claude-haiku-5-5",
    "openai": "gpt-4o-mini",
}


def resolve_provider() -> str:
    provider = config.LLM_PROVIDER
    if provider == "auto":
        if os.getenv("ANTHROPIC_API_KEY"):
            return "anthropic"
        if os.getenv("OPENAI_API_KEY"):
            return "openai"
        return "none"
    return provider


def build_chat_model() -> BaseChatModel | None:
    provider = resolve_provider()
    model = config.LLM_MODEL or DEFAULT_MODELS.get(provider)
    try:
        if provider == "anthropic":
            from langchain_anthropic import ChatAnthropic

            return ChatAnthropic(
                model=model, temperature=0, timeout=config.LLM_TIMEOUT, max_retries=1
            )
        if provider == "openai":
            from langchain_openai import ChatOpenAI

            return ChatOpenAI(
                model=model, temperature=0, timeout=config.LLM_TIMEOUT, max_retries=1
            )
    except Exception:  # pragma: no cover - misconfiguration
        log.exception("Could not initialise LLM provider %s; using rule-based mode", provider)
    return None
