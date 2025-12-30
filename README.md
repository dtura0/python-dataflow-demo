# Data Synchronization Pipeline

This project implements a small batch data pipeline that synchronizes product data from CSV files into a PostgreSQL database.

The goal is to demonstrate a **clean, testable and reproducible workflow**, including data validation, staging tables, upserts, deletes and logging.

---

## How to run the project

### Initialize the environment

```bash
make init
```

This will:

- build the application Docker image
- start PostgreSQL containers (app and test databases)
- prepare the environment for running the app and tests

### Run the application

```bash
make run
```

The application will:
- load CSV files from data/raw
- validate the data
- synchronize products into the database

## How to run the tests

```bash
make test
```

The test suite covers different layers of the application:

- Ingestion tests (test_ingest)
    - test CSV loading logic
    - focus on file handling and pandas behavior

- Validation tests (test_validations)
    - test data validation rules
    - ensure invalid rows are correctly filtered or rejected

- Database tests (test_db)
    - run against a real PostgreSQL database
    - verify real SQL behavior (upserts, deletes, constraints)
    - each test runs inside a transaction and is rolled back

## Workflow explanation

### CSV loading
CSV files are loaded using pandas, ensuring fast and reliable parsing.

### Data validation
Validation is implemented with pandas:
- schema checks
- required fields
- type coercion
- invalid rows are filtered out
- validation errors are logged

### Data synchronization
The sync_products function performs:
- creation of a temporary staging table
- upsert (INSERT ... ON CONFLICT DO UPDATE) into products
- deletion of products missing from staging
This ensures the database always reflects the latest CSV state.

### Logging
- Inserted, updated and deleted products are logged
- Errors are logged with full stack traces
- Logging is centralized and configurable


## Technical decisions

### Dockerized environment
The entire application stack is fully containerized using Docker and Docker Compose.

This ensures:
- identical behavior across environments (no “works on my machine” issues)
- zero local setup beyond Docker itself
- clear isolation between application runtime and test execution
- reproducible database state for both development and testing

### Code formatting with Black
Black enforces a consistent code style automatically, removing formatting concerns from development.

### Linting with Flake8
Flake8 is used to catch:
- unused imports
- potential bugs
- style issues

### Dependency management with pyproject.toml
Dependencies are installed directly from pyproject.toml, following modern Python standards and replacing requirements.txt.

So the **requirements.txt** and the **requirements-dev.txt** have been added only because they were requested.

### Test-driven development
The code was developed and validated through tests:
- behavior is verified before refactoring
- edge cases are explicitly tested
- confidence in correctness is increased

### Makefile
The Makefile simplifies and standardizes common tasks, ensuring consistent and easy command execution across different environments.

## Summary

This project focuses on correctness, clarity and reproducibility, providing a solid foundation for more complex data pipelines.
