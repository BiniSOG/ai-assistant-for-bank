"""FastAPI entry point (Vercel Python serverless function + local dev server).

Local:   uvicorn api.index:app --reload   →  http://localhost:8000
Vercel:  every /api/* request is rewritten to this function (see vercel.json);
         the UI in /public is served by Vercel's CDN.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Literal

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi import FastAPI, HTTPException  # noqa: E402
from fastapi.responses import FileResponse  # noqa: E402
from fastapi.staticfiles import StaticFiles  # noqa: E402
from pydantic import BaseModel, Field  # noqa: E402

from bank_assistant import agent  # noqa: E402
from bank_assistant.state import InvalidState, OnboardingState, load, sign  # noqa: E402
from bank_assistant.validators import format_fan  # noqa: E402

app = FastAPI(title="Dashen Bank AI Account Assistant", version="1.0.0")


class StartRequest(BaseModel):
    lang: Literal["en", "am"] = "en"


class SignedRequest(BaseModel):
    state: dict[str, Any]
    token: str


class ChatRequest(SignedRequest):
    message: str = Field(min_length=1, max_length=500)


class OtpRequest(SignedRequest):
    code: str = Field(max_length=20)


class ReviewRequest(SignedRequest):
    action: Literal["confirm", "edit"]


def _public_state(state: OnboardingState) -> dict[str, Any]:
    """What the UI needs to render (secrets such as the OTP hash stay in `state`)."""
    ident = state.identity
    return {
        "step": state.step,
        "lang": state.lang,
        "full_name": state.full_name,
        "date_of_birth": state.date_of_birth,
        "birth_city": state.birth_city,
        "nationality": state.nationality,
        "account_type": state.account_type,
        "fan": format_fan(state.fan) if state.fan else None,
        "verified": state.verified,
        "otp_expires": state.otp_expires,
        "identity": ident.model_dump() if ident and state.verified else None,
        "mismatches": state.mismatches,
    }


def _respond(state: OnboardingState, turn: agent.Turn) -> dict[str, Any]:
    return {
        "state": state.model_dump(mode="json"),
        "token": sign(state),
        "view": _public_state(state),
        "reply": turn.reply,
        "extra": turn.extra,
    }


def _load(req: SignedRequest, *steps: str) -> OnboardingState:
    try:
        state = load(req.state, req.token)
    except (InvalidState, ValueError) as exc:
        raise HTTPException(status_code=400, detail="invalid_state") from exc
    if steps and state.step not in steps:
        raise HTTPException(status_code=409, detail=f"wrong_step:{state.step}")
    return state


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "llm": agent.llm_mode()}


@app.post("/api/session/start")
def session_start(req: StartRequest) -> dict[str, Any]:
    state, turn = agent.start(req.lang)
    return _respond(state, turn)


@app.post("/api/chat")
def chat(req: ChatRequest) -> dict[str, Any]:
    state = _load(req, "greeting", "full_name", "date_of_birth", "birth_city",
                  "nationality", "account_type", "fan")
    turn = agent.handle_message(state, req.message)
    return _respond(state, turn)


@app.post("/api/otp/verify")
def otp_verify(req: OtpRequest) -> dict[str, Any]:
    state = _load(req, "otp")
    return _respond(state, agent.verify_otp(state, req.code))


@app.post("/api/otp/resend")
def otp_resend(req: SignedRequest) -> dict[str, Any]:
    state = _load(req, "otp")
    return _respond(state, agent.resend_otp(state))


@app.post("/api/review")
def review(req: ReviewRequest) -> dict[str, Any]:
    state = _load(req, "review")
    if not state.verified:
        raise HTTPException(status_code=403, detail="not_verified")
    return _respond(state, agent.review(state, req.action))


@app.post("/api/account/create")
def account_create(req: SignedRequest) -> dict[str, Any]:
    state = _load(req, "creating")
    if not state.verified:
        raise HTTPException(status_code=403, detail="not_verified")
    return _respond(state, agent.create_account(state))


# ---------------------------------------------------------------- local dev: serve the UI
PUBLIC = ROOT / "public"
if PUBLIC.is_dir():

    @app.get("/", include_in_schema=False)
    def index() -> FileResponse:
        return FileResponse(PUBLIC / "index.html")

    app.mount("/", StaticFiles(directory=PUBLIC), name="public")
