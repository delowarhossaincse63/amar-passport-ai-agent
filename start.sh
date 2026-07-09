#!/bin/sh

# Print the runtime PORT and use 8000 as a fallback.
# Railway should inject PORT dynamically, but this makes the startup explicit.

echo "Starting Amar Passport AI Agent"
echo "PORT=$PORT"

default_port=8000
if [ -z "$PORT" ]; then
  echo "PORT is not set, falling back to $default_port"
  PORT=$default_port
fi

exec uvicorn src.api.main:app --host 0.0.0.0 --port "$PORT"
