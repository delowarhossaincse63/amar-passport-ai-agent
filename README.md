# Amar Passport AI Agent

A multi-agent AI assistant for Bangladesh e-passport applicants. This repository provides a CrewAI-style workflow to guide users through eligibility checks, document verification, form completion, and appointment planning.

## 🚀 What it does

- Validates applicant eligibility rules
- Checks required document completeness
- Helps with form guidance and applicant data extraction
- Plans appointments with external tools and API integrations
- Exposes a FastAPI service for chat-based interactions

## 🧱 Built with

- Python 3.11+
- FastAPI
- Pydantic
- Uvicorn
- PyTest
- Scikit-learn

## Quick start

1. Create and activate a virtual environment.

   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the API locally:

   ```bash
   uvicorn src.api.main:app --reload --port 8001
   ```

4. Open the Swagger UI:

   ```text
   http://127.0.0.1:8001/docs
   ```

## Docker deployment

1. Build the image:

   ```bash
   docker build -t amar-passport-ai-agent .
   ```

2. Run the container:

   ```bash
   docker run -p 8000:8000 amar-passport-ai-agent
   ```

3. Or use Docker Compose:

   ```bash
   docker compose up --build
   ```

4. Access the service at:

   ```text
   http://127.0.0.1:8000/
   ```

## Environment variables

Copy `.env.example` to `.env` and fill in the required values.

- `OPENAI_API_KEY`
- `VECTOR_DB_URL`
- `APPOINTMENT_API_KEY`
- `ENVIRONMENT`

## Project structure

- `src/crew.py` — orchestrates the multi-agent workflow
- `src/api/main.py` — FastAPI entrypoint and request handlers
- `src/agents/` — domain-specific agent modules
- `src/rag/` — retrieval and knowledge base support
- `src/schemas/` — shared Pydantic models
- `src/tools/` — external integration utilities
- `tests/` — automated test coverage for agents and retrieval logic

## Tests

Run the test suite with:

```bash
pytest -q
```

## CI / GitHub Actions

This repository includes a CI workflow at `.github/workflows/ci.yml` that:

- installs dependencies
- runs tests with `pytest`
- builds a Docker image

## Render deployment

`render.yaml` is included for deploying this service on Render using Docker.

To deploy:

1. Create a Render Web Service.
2. Connect the GitHub repository.
3. Select Docker deployment.
4. Add required environment variables from `.env`.

## License

This project is released under the MIT License.
