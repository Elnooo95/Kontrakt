# syntax=docker/dockerfile:1
FROM python:3.10-slim

# Snabbare pip och bättre logs
ENV PIP_NO_CACHE_DIR=1 PYTHONUNBUFFERED=1

WORKDIR /app

# Installera beroenden
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Kopiera in backend-koden
COPY backend/ /app/

# Railway ger en PORT-variabel – använd den
CMD ["sh", "-c", "python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]