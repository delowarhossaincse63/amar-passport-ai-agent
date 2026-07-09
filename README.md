# Amar Passport AI Agent

A compact, professional multi-agent assistant that guides Bangladesh e-passport applicants through eligibility checks, document verification, form drafting, and appointment planning.

--

**Highlights**

- Small, focused FastAPI service with a multi-agent coordination layer.
- Local TF-IDF RAG retriever for knowledge lookup.
- Simple form-drafting agent and eligibility rules (including minor handling).
- Docker-ready and CI-friendly; Render deployment supported via `render.yaml`.

--

**Quick Start (Local)**

1. Create and activate a Python virtual environment.

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1   # PowerShell
# or: source .venv/bin/activate  # macOS / Linux
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Prepare environment variables:

Create a `.env` file (do NOT commit it) and add required keys. Example in `.env.example`.

```text
OPENAI_API_KEY=
VECTOR_DB_URL=
APPOINTMENT_API_KEY=
ENVIRONMENT=development
```

4. Run the API (development):

```powershell
.\\.venv\\Scripts\\python.exe -m uvicorn src.api.main:app --reload --host 127.0.0.1 --port 8001
```

5. Open the API docs: `http://127.0.0.1:8001/docs`

--

**Testing**

Run the project tests:

```powershell
.\\.venv\\Scripts\\python.exe -m pytest -q
```

All core tests should pass before pushing changes.

--

**Docker (optional)**

Build and run with Docker:

```bash
docker build -t amar-passport-ai-agent .
docker run -p 8000:8000 amar-passport-ai-agent
# or use docker-compose: docker compose up --build
```

--

**Deployment (Render)**

This repo includes `render.yaml` to support Render's Docker deployment. Steps:

1. Create a public or private repo on GitHub and push the code.
2. Create a new Web Service on Render and connect your GitHub repo.
3. Choose Docker, set branch to `main`, and add required environment variables in Render (e.g. `OPENAI_API_KEY`).

--

**Project Layout (short)**

- `src/api` — FastAPI routes and server entrypoint
- `src/agents` — Coordinator and specialist agents (eligibility, form filling, fee/appointment)
- `src/rag` — simple TF-IDF retriever and data files
- `src/schemas` — Pydantic models used across agents
- `tests` — unit and integration smoke tests

--

**Contributing**

- Keep changes small and focused. Run `pytest` locally before opening a PR.
- Follow existing code style. Add tests for any new behavior.

--

**Security & Secrets**

- Never commit `.env` or secret keys. Use `.env.example` as template.
- If a secret is ever committed, rotate it immediately (OpenAI keys, API keys, etc.).

--

**Contact / Author**

Delowar Hossain — link your GitHub profile or email here.

--

Thank you for checking out the project — concise, practical, and ready for deployment.
