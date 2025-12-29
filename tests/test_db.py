from decimal import Decimal

import pandas as pd
from sqlalchemy import text

from project.db import sync_products


def test_sync_products_inserts_new_products(connection, products_table):
    # GIVEN
    df = pd.DataFrame(
        {
            "product_id": [1],
            "title": ["A"],
            "price": [11.0],
            "store_id": [[2, 4]],
        }
    )

    # WHEN
    sync_products(connection, df)

    # THEN
    result = connection.execute(
        text("SELECT product_id, title, price, store_id FROM products")
    ).fetchall()

    assert result == [(1, "A", Decimal("11.0"), [2, 4])]


def test_update_product(connection):
    # GIVEN
    connection.execute(
        text(
            """
            INSERT INTO products (product_id, title, price, store_id)
            VALUES (1, 'Old title', 10.0, ARRAY[1])
            """
        )
    )

    new_df = pd.DataFrame(
        {
            "product_id": [1],
            "title": ["New title"],
            "price": [9.99],
            "store_id": [[1, 2]],
        }
    )

    # WHEN
    sync_products(connection, new_df)

    # THEN
    result = connection.execute(
        text(
            "SELECT title, price, store_id FROM products WHERE product_id = 1"  # NOQA: E501
        )
    ).one()

    assert result == ("New title", Decimal("9.99"), [1, 2])


def test_sync_products_deletes_missing_products(connection):
    # GIVEN: product exists in DB
    connection.execute(
        text(
            """
            INSERT INTO products (product_id, title, price, store_id)
            VALUES (1, 'A', 9.99, ARRAY[1])
            """
        )
    )

    # AND: empty staging
    empty_df = pd.DataFrame(
        columns=["product_id", "title", "price", "store_id"]
    )

    # WHEN
    sync_products(connection, empty_df)

    # THEN
    result = connection.execute(text("SELECT * FROM products")).fetchall()

    assert result == []


def test_logs_updated_product(connection, caplog):
    # GIVEN
    connection.execute(
        text(
            """
            INSERT INTO products (product_id, title, price, store_id)
            VALUES (1, 'Old', 10.0, ARRAY[1])
            """
        )
    )

    # WHEN
    df = pd.DataFrame(
        {
            "product_id": [1],
            "title": ["New"],
            "price": [20.0],
            "store_id": [[2]],
        }
    )

    # THEN
    with caplog.at_level("INFO"):
        sync_products(connection, df)

    assert "Updated product 1" in caplog.text


def test_products_staging_is_dropped_after_commit(engine):
    # GIVEN
    df = pd.DataFrame(
        {
            "product_id": [1],
            "title": ["A"],
            "price": [10.0],
            "store_id": [[1]],
        }
    )

    # WHEN
    with engine.begin() as conn:
        sync_products(conn, df)

        # THEN
        table = conn.execute(
            text(
                """
                SELECT to_regclass('pg_temp.products_staging')
                """
            )
        ).scalar()

        assert table == "products_staging"

    # WHEN new connection
    with engine.connect() as conn:
        table = conn.execute(
            text(
                """
                SELECT to_regclass('pg_temp.products_staging')
                """
            )
        ).scalar()

        # THEN
        assert table is None
