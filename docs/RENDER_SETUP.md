Render auto-deploy setup
=======================

This document describes how to enable automatic deploys on Render for this repository.

Two approaches are supported:

1. Native Render GitHub integration (recommended)
2. GitHub Action trigger that calls Render's deploy API (included)

Native Render integration (recommended)
-------------------------------------

1. Log in to https://render.com and create a new Web Service.
2. Choose "Connect a repository" and pick this GitHub repository.
3. Select "Docker" as the environment and ensure `render.yaml` is present (this repo includes one).
4. Set the branch to `main` and enable auto-deploy from GitHub.
5. In Render's dashboard, add environment variables shown in `render.yaml` (OPENAI_API_KEY, VECTOR_DB_URL, APPOINTMENT_API_KEY, ENVIRONMENT).

Render will read `render.yaml` and use the specified Dockerfile and start command. Each push to `main` will trigger a deploy automatically.

Using the GitHub Action trigger (alternative)
-------------------------------------------

This repository includes `.github/workflows/render-deploy.yml`, which will call the Render Deploy API on each push to `main` if the following repository secrets are set:

- `RENDER_API_KEY` — a Render API key with `deploys:write` permission (create via Render dashboard → Account → API Keys).
- `RENDER_SERVICE_ID` — your Render Service ID (found in the URL or Render service settings).

To set secrets:

1. In GitHub, go to Settings → Secrets → Actions and add `RENDER_API_KEY` and `RENDER_SERVICE_ID`.
2. Push to `main`; the workflow will POST to `https://api.render.com/v1/services/{serviceId}/deploys` to trigger a build.

Notes
-----
- The native Render integration is simpler and recommended — Render will handle builds, logs, and persistent env vars.
- The GitHub Action is a lightweight alternative when you prefer to manage deploy triggers from CI.
- If you also use the Docker publish workflow (`.github/workflows/docker-ci.yml`), you can push images to GHCR and reference them from Render if desired.
