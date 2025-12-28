import logging
from sqlalchemy import create_engine
from sqlalchemy import text


logger = logging.getLogger(__name__)


def get_engine(db_url):
    return create_engine(db_url)


def sync_products(engine):
    with engine.begin() as connection:
        update_products(connection)
        insert_products(connection)
        delete_products(connection)


def update_products(conn):
    try:
        updated = conn.execute(
            text(
                """UPDATE products p
                    SET
                        name = s.name,
                        price = s.price,
                        store_id = s.store_id::INT[]
                    FROM products_staging s
                    WHERE p.product_id = s.product_id
                    RETURNING p.product_id;"""
            )
        )
        for (product_id,) in updated:
            logger.info("Updated product %s", product_id)
    except Exception:
        logger.exception("Error updating products")
        raise


def insert_products(conn):
    try:
        inserted = conn.execute(
            text(
                """
                INSERT INTO products
                SELECT
                    s.product_id,
                    s.name,
                    s.price,
                    s.store_id::INT[]
                FROM products_staging s
                LEFT JOIN products p USING (product_id)
                WHERE p.product_id IS NULL
                RETURNING product_id;
            """
            )
        )
        for (product_id,) in inserted:
            logger.info("Inserted product %s", product_id)
    except Exception:
        logger.exception("Error inserting products")
        raise


def delete_products(conn):
    try:
        deleted = conn.execute(
            text(
                """
                DELETE FROM products
                WHERE product_id NOT IN (
                    SELECT product_id FROM products_staging
                )
                RETURNING product_id;"""
            )
        )
        for (product_id,) in deleted:
            logger.info("Deleted product %s", product_id)
    except Exception:
        logger.exception("Error deleting products")
        raise


def write_staging(df, engine):
    df.to_sql(
        name="products_staging",
        con=engine,
        if_exists="replace",
        index=False,
    )
    logger.info("Loaded %d rows into products_staging", len(df))
