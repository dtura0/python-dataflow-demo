import logging
import pandas as pd

from project.config import DATA_DIR


logger = logging.getLogger(__name__)


def load_csv(path):
    logger.info("Loading CSV file: %s", path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    df = pd.read_csv(path, encoding="utf-8", dtype=str)

    logger.info("Loaded %d rows from %s", len(df), path)
    return df
