import os
from pathlib import Path


DATA_DIR = Path("data/raw")
CSV_FILES = [
    "feed_items.csv",
    "portal_items.csv",
]
DB_URL = os.getenv(
    "DB_URL", "postgresql+psycopg2://user:password@localhost:5432/p"
)
