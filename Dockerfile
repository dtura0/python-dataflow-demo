FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./

RUN pip install --upgrade pip \
    && pip install -e ".[dev]"

COPY src ./src

COPY data ./data

COPY tests ./tests

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "project.main"]
