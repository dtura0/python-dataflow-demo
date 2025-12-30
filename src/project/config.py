import os
from pathlib import Path


DATA_DIR = Path("data/raw")
CSV_FILES = [
    "feed_items.csv",
    "portal_items.csv",
]
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql+psycopg2://user:password@db:5432/db"
)
