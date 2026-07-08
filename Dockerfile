FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

# Default port used at runtime; Railway and other hosts set `PORT` dynamically.
ENV PORT=8000

# EXPOSE is informational; keep 8000 as the default build-time exposed port.
EXPOSE 8000

# Use shell form so the `$PORT` env var is expanded at container start.
# Railway / other platforms set the `PORT` env var at runtime.
CMD uvicorn src.api.main:app --host 0.0.0.0 --port $PORT
