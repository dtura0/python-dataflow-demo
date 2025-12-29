import logging
from sqlalchemy import create_engine
from sqlalchemy import text


logger = logging.getLogger(__name__)


def get_engine(db_url):
    return create_engine(db_url)


def write_staging(conn, df):
    conn.execute(
        text(
            """
            CREATE TEMP TABLE IF NOT EXISTS products_staging (
                product_id INT,
                title TEXT,
                price NUMERIC,
                store_id INT[]
            ) ON COMMIT DROP
            """
        )
    )

    df.to_sql(
        name="products_staging",
        con=conn,
        if_exists="append",
        index=False,
    )

    logger.info("Loaded %d rows into products_staging", len(df))


def upsert_products(conn):
    try:
        result = conn.execute(
            text(
                """
                INSERT INTO products (product_id, title, price, store_id)
                SELECT
                    s.product_id::INT,
                    s.title,
                    s.price::NUMERIC,
                    s.store_id::INT[]
                FROM products_staging s
                ON CONFLICT (product_id) DO UPDATE
                SET
                    title = EXCLUDED.title,
                    price = EXCLUDED.price,
                    store_id = EXCLUDED.store_id
                RETURNING
                    product_id,
                    (xmax = 0) AS inserted;
                """
            )
        )

        for product_id, inserted in result:
            if inserted:
                logger.info("Inserted product %s", product_id)
            else:
                logger.info("Updated product %s", product_id)

    except Exception:
        logger.exception("Error upserting products")
        raise


def delete_products(conn):
    try:
        deleted = conn.execute(
            text(
                """
                DELETE FROM products p
                WHERE NOT EXISTS (
                    SELECT 1
                    FROM products_staging s
                    WHERE s.product_id = p.product_id
                )
                RETURNING p.product_id;"""
            )
        )
        for (product_id,) in deleted:
            logger.info("Deleted product %s", product_id)
    except Exception:
        logger.exception("Error deleting products")
        raise


def sync_products(connection, df):
    write_staging(connection, df)
    upsert_products(connection)
    delete_products(connection)
