# syntax=docker/dockerfile:1

# ------------------------------
# Base image
# ------------------------------
FROM python:3.12-slim AS base

# Avoid .pyc files and enable unbuffered stdout
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System packages (curl for healthchecks/logs)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 10001 appuser

# Working directory
WORKDIR /app

# ------------------------------
# Python dependencies
# ------------------------------
# Copy only dependency files first to leverage Docker layer caching
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install deps without cache
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# ------------------------------
# Application code
# ------------------------------
# Copy the application source
COPY app /app/app

# Copy Alembic configuration and migration scripts
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic

# Optional: copy .env only if you want baked defaults (prefer --env-file at runtime)
# COPY .env /app/.env

# Expose app port (container side)
EXPOSE 8000

# Switch to unprivileged user
USER appuser

# Healthcheck against a lightweight endpoint
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD curl -fsS http://127.0.0.1:8000/health || exit 1

# ------------------------------
# Entrypoint (Gunicorn with Uvicorn workers)
# ------------------------------
# Notes:
# - ASGI: use UvicornWorker to serve FastAPI
# - Replace "app.main:app" if your module path differs
CMD ["gunicorn", "app.main:app", \
     "-k", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "2", \
     "--timeout", "60"]
