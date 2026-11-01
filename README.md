# Dashen Bank – AI Video Account Assistant

An AI assistant that opens a bank account over a "video call", built with **Python, LangChain and FastAPI**. It follows the 10-step flow in the design:

| # | Screen | What happens |
|---|--------|--------------|
| 1 | Super App home | Tap **Create Account** (EN / አማርኛ toggle) |
| 2 | Video call starts | The AI avatar greets the customer in English or Amharic (speech synthesis) |
| 3 | Q1 – Full name | The customer speaks (browser speech-to-text) or types |
| 4 | Q2 – Date of birth | Say it or pick it from a date picker. Must be 18 or older |
| 5 | Q3 – Birth city | Then nationality and account type (chips, typing or voice) |
| 6 | National ID | Enter the 12-digit **FAN** (Fayda ID number) |
| 7 | OTP | A 6-digit OTP goes to the phone registered with the National ID, with a resend countdown |
| 8 | Review | Shows the details retrieved from the National ID registry and flags anything that differs from the customer's answers |
| 9 | Creating account | Progress checklist |
| 10 | Success | Account number (copy button), account type, download of the account details |

## Architecture

```
public/            Static mobile UI (HTML/CSS/vanilla JS): avatar, TTS, STT, camera self-view
api/index.py       FastAPI app → Vercel Python serverless function (all /api/* routes)
bank_assistant/
  agent.py         LangChain interpretation chain + conversation state machine
  llm.py           Chat-model factory (Anthropic or OpenAI via LangChain)
  validators.py    Deterministic parsing and validation (names, dates, cities, FAN, OTP…)
  messages.py      English and Amharic script
  registry.py      Mock National ID (Fayda) lookup and OTP service  ← replace with real APIs
  accounts.py      Mock core-banking account creation                ← replace with real API
  state.py         Signed (HMAC) conversation state
tests/             End-to-end API tests
```

**LangChain usage.** Each customer utterance runs through

```python
(prompt | chat_model.with_structured_output(TurnInterpretation))
    .with_fallbacks([RunnableLambda(rule_based_interpret)])
```

The LLM handles free-form speech ("I was born in Addis, near Piassa"). It notices when the customer asks a question instead of answering, answers it, and then asks the original question again. It also pulls out the field value. The result always goes through the Python validators before it is accepted. If no API key is set, or the LLM call fails, the rule-based interpreter takes over, so the demo works with **zero configuration**.

**Serverless-friendly.** Vercel functions are stateless. The conversation state therefore travels with the browser and is **HMAC-signed**, so a customer can't skip OTP verification by editing it. The OTP is stored only as an HMAC hash.

## Test data

* FAN `1234 5678 9012` → Betelhem Tesfaye Alemu, 15 Jan 2000, Addis Ababa
* FAN `9876 5432 1098` → Abebe Kebede Bekele, 3 Jun 1992, Bahir Dar
* Any other 12-digit FAN is "found" using the answers you gave.
* No SMS gateway is connected, so the OTP appears in a yellow **demo banner** (`DEMO_SHOW_OTP=true`).

Voice input works in Chrome and Edge, and camera and mic need HTTPS (Vercel provides it). You can always type instead.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
uvicorn api.index:app --reload        # http://localhost:8000
pytest -q
```

## Deploy to Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2FBiniSOG%2FAI_Assistant_for_Bank&env=APP_SECRET&envDescription=Random%20secret%20used%20to%20sign%20sessions)

Or do it by hand:

1. On vercel.com, go to **Add New → Project** and import `BiniSOG/AI_Assistant_for_Bank`. Pick the branch to deploy (Production uses the default branch; preview deployments are created for other branches).
2. Leave Framework Preset set to **Other** and leave the build settings empty. `vercel.json` routes `/api/*` to the Python function, and `public/` is served as static files.
3. Add these environment variables:
   * `APP_SECRET`: a long random string (**required**)
   * `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`: optional, turns on the LLM
   * `LLM_MODEL`: optional model override
   * `DEMO_SHOW_OTP`: set it to `false` once a real SMS gateway is connected
4. Click **Deploy**.

CLI alternative: `npm i -g vercel && vercel --prod`.

## Going to production

* `registry.lookup_identity` → the Fayda / NIDP eKYC API
* `registry.send_otp` → SMS gateway (or the Fayda OTP endpoint)
* `accounts.create_account` → core banking (CBS) account opening API
* Add liveness and face-match checks against the National ID photo, using the camera stream that is already on screen
