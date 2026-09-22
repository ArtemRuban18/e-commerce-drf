FROM python:3.12-alpine AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .

RUN apt-get update & apt-get install -y --no-install-recommends \
    build-esential \
    gcc \ 
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r --no-cache-dir requirements.txt

FROM python:3.12-alpine

