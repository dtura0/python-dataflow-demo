import pytest
from sqlalchemy import create_engine, text

TEST_DB_URL = "postgresql://user:password@localhost:5433/test_db"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_DB_URL)
    yield engine
    engine.dispose()


@pytest.fixture
def connection(engine, products_table):
    connection = engine.connect()
    transaction = connection.begin()

    try:
        yield connection
    finally:
        transaction.rollback()
        connection.close()


@pytest.fixture(scope="session")
def products_table(engine):
    with engine.begin() as conn:
        conn.execute(text("DROP TABLE IF EXISTS products"))
        conn.execute(
            text(
                """
                CREATE TABLE products (
                    product_id INT PRIMARY KEY,
                    name TEXT,
                    price NUMERIC,
                    store_id INT[]
                )
                """
            )
        )
    yield
