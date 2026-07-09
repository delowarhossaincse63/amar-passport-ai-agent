FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

COPY . .

# Default port used at runtime; Railway and other hosts set `PORT` dynamically.
ENV PORT=8000

# EXPOSE is informational; keep 8000 as the default build-time exposed port.
EXPOSE 8000

# Make the startup script executable and use it for runtime port resolution.
RUN chmod +x /app/start.sh

CMD ["/bin/sh", "/app/start.sh"]
