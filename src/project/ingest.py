import logging
import pandas as pd
from pathlib import Path


logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "raw"


def load_csv(filename):
    path = DATA_DIR / filename

    logger.info("Loading CSV file: %s", path)

    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    df = pd.read_csv(path, encoding="utf-8", dtype=str)

    logger.info("Loaded %d rows from %s", len(df), filename)
    return df
