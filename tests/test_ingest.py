import pandas as pd
import pytest

from project import config
from project import ingest


def test_load_csv_valid_file(tmp_path, monkeypatch):
    data_dir = tmp_path / "data" / "raw"
    data_dir.mkdir(parents=True)

    csv_file = data_dir / "test.csv"
    csv_file.write_text(
        "product_id,title,price,store_id\n" "1,A,9.99,2|4\n" "2,B,19.99,3\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(config, "DATA_DIR", data_dir)

    df = ingest.load_csv(csv_file)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df.columns) == ["product_id", "title", "price", "store_id"]
    assert df.iloc[0]["product_id"] == "1"


def test_load_csv_file_not_found(tmp_path, monkeypatch):
    data_dir = tmp_path / "data" / "raw"
    data_dir.mkdir(parents=True)

    monkeypatch.setattr(config, "DATA_DIR", data_dir)

    with pytest.raises(FileNotFoundError) as exc:
        ingest.load_csv(data_dir / "missing.csv")

    assert "CSV file not found" in str(exc.value)
