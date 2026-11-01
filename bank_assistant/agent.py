"""The LangChain-powered onboarding agent.

Each customer utterance is passed through an *interpretation chain*:

    ChatPromptTemplate | ChatModel.with_structured_output(TurnInterpretation)
        .with_fallbacks([RunnableLambda(rule_based_interpret)])

The LLM understands free-form speech ("uh, I was born in Addis, near Piassa"),
detects off-script questions and answers them, and extracts the field value.
If no LLM is configured, or the LLM call fails/times out, the deterministic
rule-based interpreter takes over so the flow always works. Every extracted
value is then validated in Python (validators.py) before it is accepted.
"""
from __future__ import annotations

import logging
import random
from dataclasses import dataclass, field
from functools import lru_cache
from typing import Any, Literal

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda
from pydantic import BaseModel, Field

from . import accounts, config, registry
from .llm import build_chat_model
from .messages import ACKS, t
from .state import QUESTION_STEPS, OnboardingState
from .validators import PARSERS, format_fan, parse_otp, yes_no

log = logging.getLogger(__name__)


class TurnInterpretation(BaseModel):
    """How the customer's latest message relates to the current question."""

    intent: Literal["answer", "affirm", "deny", "question", "other"] = Field(
        description=(
            "answer = the message answers the current question; affirm/deny = yes/no; "
            "question = the customer asks something instead of answering; other = anything else"
        )
    )
    value: str | None = Field(
        default=None,
        description="The extracted value for the requested field, normalised as described. Null if not given.",
    )
    reply: str | None = Field(
        default=None,
        description=(
            "Only when intent is 'question': a short, friendly answer (max 2 sentences) "
            "in the conversation language. Do not repeat the current question."
        ),
    )


FIELD_SPECS: dict[str, str] = {
    "greeting": "Whether the customer agrees to start opening an account (affirm / deny). No value.",
    "full_name": "The customer's full name (given name, father's name and optionally grandfather's name). Return just the name.",
    "date_of_birth": "Date of birth in Gregorian calendar, returned as ISO YYYY-MM-DD. If an Ethiopian-calendar date is clearly stated, convert it to Gregorian.",
    "birth_city": "The city where the customer was born, returned as the common English city name (e.g. 'Addis Ababa').",
    "nationality": "The customer's nationality as a demonym in English (e.g. 'Ethiopian').",
    "account_type": "One of exactly: 'Savings Account', 'Current Account', 'Interest-Free (Wadiah) Savings', 'Fixed Time Deposit'.",
    "fan": "The 12-digit Fayda National ID number (FAN). Return digits only; convert spoken digits to numerals.",
}

SYSTEM_PROMPT = """You are the Dashen Bank AI Account Assistant, a friendly video-call agent \
that helps customers in Ethiopia open a bank account in the Dashen Bank Super App.
The conversation language is {language}.

You are currently asking for: {step}
Field specification: {field_spec}

Interpret the customer's latest message and return the structured result.
- Extract the value only if the customer actually provided it. Never invent values.
- Speech-to-text transcripts may contain filler words or minor errors; be tolerant.
- If the customer asks a question, set intent to 'question' and give a brief helpful reply.
  You can explain the process (questions, then National ID/Fayda verification with an OTP sent \
to the phone registered with the National ID, then review and account creation). If you don't know \
a bank-specific policy (fees, rates, limits), say a Dashen Bank branch officer can help.
- Never ask for passwords, PINs or card numbers."""


def rule_based_interpret(inp: dict[str, Any]) -> TurnInterpretation:
    step, msg = inp["step"], (inp["message"] or "").strip()
    yn = yes_no(msg)
    is_question = msg.endswith("?") or msg.endswith("፧")
    if step == "greeting":
        if yn == "deny":
            return TurnInterpretation(intent="deny")
        if is_question and yn is None:
            return TurnInterpretation(intent="question")
        return TurnInterpretation(intent="affirm")
    parser = PARSERS.get(step)
    if is_question and parser and not parser(msg).ok:
        return TurnInterpretation(intent="question")
    return TurnInterpretation(intent="answer", value=msg)


@lru_cache(maxsize=1)
def interpretation_chain() -> Runnable:
    rules = RunnableLambda(rule_based_interpret, name="rule_based_interpreter")
    llm = build_chat_model()
    if llm is None:
        log.info("No LLM configured – using rule-based interpreter")
        return rules
    prompt = ChatPromptTemplate.from_messages(
        [("system", SYSTEM_PROMPT), ("human", "{message}")]
    )
    to_prompt_vars = RunnableLambda(
        lambda inp: {
            "language": "Amharic" if inp["lang"] == "am" else "English",
            "step": inp["step"],
            "field_spec": FIELD_SPECS.get(inp["step"], ""),
            "message": inp["message"],
        }
    )
    llm_chain = to_prompt_vars | prompt | llm.with_structured_output(TurnInterpretation)
    return llm_chain.with_fallbacks([rules])


def llm_mode() -> str:
    from .llm import resolve_provider

    return resolve_provider()


# --------------------------------------------------------------------------- turn handling
@dataclass
class Turn:
    reply: str
    extra: dict[str, Any] = field(default_factory=dict)


def question_for(state: OnboardingState) -> str:
    if state.step == "greeting":
        return t(state.lang, "greeting")
    first = (state.full_name or "").split(" ")[0]
    return t(state.lang, f"ask_{state.step}", first_name=first)


def _next_step(step: str) -> str:
    i = QUESTION_STEPS.index(step)
    return QUESTION_STEPS[i + 1]


def start(lang: str = "en") -> tuple[OnboardingState, Turn]:
    state = OnboardingState(lang="am" if lang == "am" else "en")
    return state, Turn(question_for(state))


def handle_message(state: OnboardingState, message: str) -> Turn:
    if state.step != "greeting" and state.step not in QUESTION_STEPS:
        raise ValueError(f"step {state.step!r} does not accept chat messages")

    interp: TurnInterpretation = interpretation_chain().invoke(
        {"step": state.step, "message": message, "lang": state.lang}
    )

    if interp.intent == "question":
        answer = interp.reply or t(state.lang, "fallback_question")
        return Turn(f"{answer} {question_for(state)}")

    if state.step == "greeting":
        if interp.intent == "deny":
            return Turn(t(state.lang, "greeting_deny"))
        state.step = "full_name"
        return Turn(question_for(state))

    parser = PARSERS[state.step]
    parsed = parser(interp.value) if interp.value else None
    if not (parsed and parsed.ok):
        raw = parser(message)
        parsed = raw if raw.ok or parsed is None else parsed
    if not parsed.ok:
        err = t(state.lang, parsed.error or "fallback_question", min_age=config.MIN_AGE)
        return Turn(err)

    setattr(state, state.step, parsed.value)

    if state.step == "fan":
        return _issue_otp(state)

    state.step = _next_step(state.step)
    # Some prompts already open with an acknowledgement ("Thank you…", "Got it…").
    has_ack = state.step in ("date_of_birth", "birth_city", "nationality")
    ack = "" if has_ack else random.choice(ACKS[state.lang]) + " "
    return Turn(ack + question_for(state), {"captured": parsed.value})


def _issue_otp(state: OnboardingState) -> Turn:
    identity = registry.lookup_identity(state.fan, state)
    state.identity = identity
    state.verified = False
    code = registry.send_otp(state)
    state.step = "otp"
    phone = registry.mask_phone(identity.phone)
    extra: dict[str, Any] = {"phone": phone, "fan": format_fan(state.fan)}
    if config.DEMO_SHOW_OTP:
        extra["demo_otp"] = code
    return Turn(t(state.lang, "otp_sent", phone=phone), extra)


def resend_otp(state: OnboardingState) -> Turn:
    turn = _issue_otp(state)
    turn.reply = t(state.lang, "otp_resent", phone=turn.extra["phone"])
    return turn


def verify_otp(state: OnboardingState, code: str) -> Turn:
    otp = parse_otp(code)
    result = registry.check_otp(state, otp) if otp else "bad"
    if result == "ok":
        state.verified = True
        state.step = "review"
        state.otp_hash = None
        state.mismatches = _mismatches(state)
        return Turn(t(state.lang, "otp_ok"), {"verified": True})
    if result == "locked":
        state.step = "fan"
        state.otp_hash = None
        return Turn(t(state.lang, "otp_locked"), {"locked": True})
    if result == "expired":
        return Turn(t(state.lang, "otp_expired"), {"expired": True})
    left = max(config.OTP_MAX_ATTEMPTS - state.otp_attempts, 0)
    return Turn(t(state.lang, "otp_bad", left=left))


def _mismatches(state: OnboardingState) -> list[str]:
    """Fields where what the customer said differs from the National ID record."""
    rec = state.identity
    if not rec:
        return []
    out = []
    norm = lambda s: " ".join((s or "").lower().split())  # noqa: E731
    if norm(rec.full_name) != norm(state.full_name):
        out.append("full_name")
    if rec.date_of_birth != state.date_of_birth:
        out.append("date_of_birth")
    if norm(rec.birth_city) != norm(state.birth_city):
        out.append("birth_city")
    return out


def review(state: OnboardingState, action: str) -> Turn:
    if action == "edit":
        state.step = "account_type"
        state.verified = False
        state.identity = None
        state.mismatches = []
        return Turn(t(state.lang, "review_edit"))
    state.step = "creating"
    return Turn(t(state.lang, "creating"))


def create_account(state: OnboardingState) -> Turn:
    state.account_number = accounts.create_account(state)
    state.step = "done"
    return Turn(
        t(state.lang, "done"),
        {
            "account_number": accounts.format_account_number(state.account_number),
            "account_type": state.account_type,
            "progress": [
                "Verifying identity (National ID)",
                "Retrieving your details",
                "Creating Dashen Bank account",
                "Setting up your profile",
            ],
        },
    )
