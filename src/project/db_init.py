from sqlalchemy import create_engine, text

from project.config import DB_URL


def main():
    engine = create_engine(DB_URL)

    with engine.begin() as conn:
        conn.execute(
            text(
                """
                CREATE TABLE IF NOT EXISTS products (
                    product_id INT PRIMARY KEY,
                    title TEXT,
                    price NUMERIC,
                    store_id INT[]
                )
                """
            )
        )


if __name__ == "__main__":
    main()
