FROM python:3.13-slim

WORKDIR /app

# System deps (psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency definition
COPY pyproject.toml ./

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -e ".[dev]"

# Copy source code
COPY src ./src

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "project.main"]
