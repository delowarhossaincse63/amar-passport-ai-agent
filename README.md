# Amar Passport AI Agent

A CrewAI-style multi-agent system for guiding Bangladesh e-passport applicants through eligibility, document checks, form guidance, and appointment planning.

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the API: `uvicorn src.api.main:app --reload --port 8001`
4. Visit `http://127.0.0.1:8001/docs` for the Swagger UI.

## Docker deployment

1. Build the image:
   ```bash
   docker build -t amar-passport-ai-agent .
   ```
2. Run the container:
   ```bash
   docker run -p 8000:8000 amar-passport-ai-agent
   ```
3. Or use docker-compose:
   ```bash
   docker compose up --build
   ```
4. Access the live app at `http://127.0.0.1:8000/`.

## Project structure

- `src/agents` - specialist agents
- `src/tools` - optional integrations
- `src/rag` - retrieval layer and knowledge base scaffolding
- `src/schemas` - shared Pydantic models
- `src/api` - FastAPI entrypoint
- `tests` - smoke tests for the initial scaffolding

## CI / GitHub

This repository includes a GitHub Actions workflow to run tests and build the Docker image on push or pull request. To enable continuous deployment, add a registry secret and update the workflow to push the built image to GitHub Container Registry or your cloud provider.

Quick steps to enable CI on GitHub:

1. Create a repository on GitHub and push this project.
2. Enable Actions in the repository settings (workflows are already included at `.github/workflows/ci.yml`).
3. (Optional) Add repository secrets for `CR_PAT` or registry credentials if you want to push images.

## Render deployment

This repo includes `render.yaml` for Render deployment using Docker.

Steps to deploy on Render:

1. Create a new Web Service on Render.
2. Connect your GitHub repository.
3. Choose the `main` branch and Docker as the environment.
4. Render will detect `render.yaml` and use the Dockerfile.
5. Add these environment variables in Render settings:
   - `OPENAI_API_KEY`
   - `VECTOR_DB_URL`
   - `APPOINTMENT_API_KEY`
   - `ENVIRONMENT=production`

Render will then build and deploy the app. The service will be live on the Render-provided URL.

Badge (replace `<OWNER>` and `<REPO>`):

![CI](https://github.com/<OWNER>/<REPO>/actions/workflows/ci.yml/badge.svg)
