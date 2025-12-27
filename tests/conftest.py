import pytest
from sqlalchemy import create_engine

TEST_DB_URL = "postgresql://user:password@localhost:5433/test_db"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DB_URL)
    yield engine
    engine.dispose()
