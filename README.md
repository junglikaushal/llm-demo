# LLM Demo — FastAPI + OpenAI

A production-style FastAPI service where a user submits a question through a browser page, the question is sent to an LLM (OpenAI), and a structured JSON answer is returned and rendered.

## Features

- FastAPI backend with a clean layered structure (routes / schemas / services)
- Structured, validated responses (answer, confidence, topic, tokens used) via Pydantic
- OpenAI integration with async calls and JSON-mode responses
- Proper HTTP error handling (502 for provider errors, 504 for timeouts, 422 for invalid input)
- Simple browser frontend calling the API directly — no separate frontend framework
- Environment-based configuration — no secrets in code

## Project structure

\`\`\`
app/
├── main.py              # app assembly: creates FastAPI app, mounts routes and static files
├── core/
│   └── config.py        # settings loaded from environment / .env
├── api/
│   └── routes.py         # HTTP endpoints (/health, /ask)
├── schemas/
│   ├── request.py        # AskRequest — validated input shape
│   └── response.py       # AskResponse — validated output shape
├── services/
│   └── llm_service.py    # OpenAI call, JSON parsing, custom exceptions
└── static/
    └── index.html         # browser frontend
\`\`\`

## Setup

**Requirements:** Python 3.10+, [uv](https://docs.astral.sh/uv/), an OpenAI API key.

\`\`\`bash
git clone https://github.com/junglikaushal/llm-demo.git
cd llm-demo
uv sync
\`\`\`

Create a \`.env\` file in the project root:

\`\`\`
OPENAI_API_KEY=sk-your-key-here
\`\`\`

## Running

\`\`\`bash
uv run uvicorn app.main:app --reload
\`\`\`

- Browser UI: http://127.0.0.1:8000/
- Interactive API docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## API

### `POST /ask`

**Request:**
\`\`\`json
{ "question": "What is FastAPI?" }
\`\`\`

**Response (200):**
\`\`\`json
{
  "answer": "FastAPI is a modern Python web framework for building APIs.",
  "confidence": 0.95,
  "topic": "Programming",
  "tokens_used": 87
}
\`\`\`

**Error responses:**
| Status | Meaning |
|--------|---------|
| 422 | Invalid request (e.g. empty question) |
| 502 | OpenAI returned an error or unparseable response |
| 504 | OpenAI request timed out |

### `GET /health`

Returns `{"status": "ok"}` — used for uptime/monitoring checks.

## Configuration

All settings are read from environment variables (or `.env` locally):

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *(required)* | Your OpenAI API key |
| `OPENAI_MODEL` | `gpt-4o-mini` | Which OpenAI model to use |
| `REQUEST_TIMEOUT` | `30.0` | Max seconds to wait for the LLM before returning a 504 |

## Design notes

- **Layered architecture** — routes handle HTTP only, services handle business logic. This keeps the LLM integration testable in isolation and makes it straightforward to swap providers later.
- **Fail fast on startup** — the app refuses to start if `OPENAI_API_KEY` is missing, rather than failing on the first request.
- **Structured errors, not stack traces** — known failure modes (timeout, provider error, invalid input) are translated into specific HTTP status codes with clear messages, so API consumers can handle them programmatically.

## Possible next steps

- Rate limiting per client
- Dockerfile for containerized deployment
- Request/response logging
- Automated test suite