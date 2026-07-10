Railway deployment guide
=======================

This document explains simple ways to deploy this Docker-based FastAPI service to Railway.

Option 1 — Connect GitHub repo directly (recommended)
--------------------------------------------------

1. Sign into https://railway.app and create a new Project.
2. Click "Deploy from GitHub" and connect your GitHub account (if not already connected).
3. Select this repository and the `main` branch.
4. Choose the Docker deployment option or let Railway detect the Dockerfile in the repo root.
5. In Railway, add environment variables (OPENAI_API_KEY, VECTOR_DB_URL, APPOINTMENT_API_KEY, ENVIRONMENT) under Project Settings → Variables.
6. Trigger a deploy by pushing to `main` or clicking Deploy in Railway UI.

Notes:
- Railway will build the image using your `Dockerfile` and run the container.
- Logs and build output are available in the Railway dashboard.

Option 2 — Deploy via Docker image (push to GHCR, then point Railway at the image)
-----------------------------------------------------------------------------------

1. Enable GitHub Actions CI to publish the Docker image to GitHub Container Registry (GHCR). This repository already contains `.github/workflows/docker-ci.yml` — set the `CR_PAT` secret in GitHub secrets.
2. Once the image is pushed to `ghcr.io/<owner>/<repo>:latest`, create a Railway project and choose "Deploy from Docker image" (or configure a service to pull the image).
3. Add environment variables in Railway and deploy.

Option 3 — Use Railway CLI from CI (advanced)
----------------------------------------------

Railway offers a CLI that can be run from CI to trigger deployments (`railway up`). This repository includes a sample workflow at `.github/workflows/railway-deploy.yml`.

Required GitHub secrets:
- `RAILWAY_TOKEN` — Railway API or project token with deploy permissions

Once the secret is set, pushes to `main` will automatically run the workflow and trigger the Railway deploy.

Security reminder
-----------------

- Do not commit secrets. Use Railway project variables or GitHub Actions secrets.
- If you previously committed an API key, rotate it immediately.

Need help?
-----------

Tell me which approach you prefer (direct GitHub integration, GHCR + image, or CLI-driven CI), and I will add any helper workflow or sample config you need.
