# syntax=docker/dockerfile:1.6
FROM python:3.11-slim AS base

# --- System setup ---
ENV VIRTUAL_ENV=/opt/venv \
    PATH=/opt/venv/bin:$PATH

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl git \
    && python -m venv "$VIRTUAL_ENV" \
    && pip install --upgrade pip setuptools wheel \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

# --- Python dependencies ---
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# --- Project source ---
COPY . .

CMD ["bash"]
