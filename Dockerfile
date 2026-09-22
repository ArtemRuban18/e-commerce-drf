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

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 
ENV PYTHONUNBUFFERED=1

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages

COPY . .
RUN adduser --disabled-password --gecos '' appuser && \
    mkdir -p /app/media /app/static && \
    chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


