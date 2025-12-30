VENV := .venv
PYTHON := $(if $(wildcard $(VENV)/bin/python),$(VENV)/bin/python,python3)
PYTHONPATH := src
PIP := $(VENV)/bin/pip

export DB_URL=postgresql://user:password@localhost:5432/db
export TEST_DB_URL=postgresql://user:password@localhost:5433/test_db

.PHONY: init run test db-start db-stop venv

venv:
	$(PYTHON) -m venv $(VENV)

install-deps:
	. $(VENV)/bin/activate && \
	$(PIP) install --upgrade pip && \
	$(PIP) install -e ".[dev]" && \
	sleep 5

db-start:
	. $(VENV)/bin/activate && \
	docker compose up -d && \
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m project.db_init

init: venv install-deps db-start
	@echo "✔ Environment ready"

run:
	PYTHONPATH=$(PYTHONPATH) $(PYTHON) -m project.main

test:
	$(PYTHON) -m pytest -v

db-stop:
	docker compose down
