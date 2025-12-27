import logging

from project.ingest import load_csv
from project.logging_config import setup_logging


logger = logging.getLogger(__name__)


def main():
    setup_logging()
    for csv in ("feed_items", "portal_items"):
        logger.info("Processing file %s", csv)

        load_csv("data.csv")

        logger.info("Finished processing file %s", csv)


if __name__ == "__main__":
    main()
