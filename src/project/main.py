import logging
import os

from project.config import DATA_DIR, CSV_FILES
from project.db import get_engine, sync_products
from project.ingest import load_csv
from project.logging_config import setup_logging
from project.validation import validate_data


logger = logging.getLogger(__name__)


def main():
    setup_logging()
    db_url = os.environ["DATABASE_URL"]
    engine = get_engine(db_url)

    for filename in CSV_FILES:
        csv_path = DATA_DIR / filename

        logger.info("Processing file %s (%s)", filename, csv_path)

        if not csv_path.exists():
            raise FileNotFoundError(f"CSV not found: {csv_path}")

        with engine.begin() as conn:
            df = load_csv(csv_path)

            validated_df = validate_data(df, filename)
            if validated_df.empty:
                raise ValueError(f"No valid rows to process for {filename}")

            sync_products(conn, validated_df)

        logger.info("Finished processing file %s", filename)


if __name__ == "__main__":
    main()
