import logging
import os

from project.db import get_engine, sync_products
from project.ingest import load_csv
from project.logging_config import setup_logging
from project.validation import validate_data


logger = logging.getLogger(__name__)


def main():
    setup_logging()
    db_url = os.environ["DATABASE_URL"]
    engine = get_engine(db_url)

    for csv in ("feed_items", "portal_items"):
        with engine.begin() as conn:
            logger.info("Processing file %s", csv)

            df = load_csv("data.csv")
            validated_df = validate_data(df)
            if validated_df.empty:
                raise ValueError("No valid rows to process for %s", csv)

            sync_products(conn, validated_df)

            logger.info("Finished processing file %s", csv)


if __name__ == "__main__":
    main()
