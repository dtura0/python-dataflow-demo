import pandas as pd
import pytest

from project.validation import validate_data


def test_fails_on_missing_column():
    df = pd.DataFrame({"product_id": [1]})
    with pytest.raises(KeyError):
        validate_data(df, "whatever")


def test_invalid_rows_are_dropped(caplog):
    df = pd.DataFrame(
        {
            "product_id": [1, 2, None, 60],
            "title": ["A", "B", "C", "D"],
            "price": ["9.99", -5, 8.75, "cheap"],
            "store_id": ["2|4", "1|3", "3", "1"],
        }
    )

    result = validate_data(df, "whatever")

    assert len(result) == 1
    assert result.iloc[0]["product_id"] == 1
    assert "Invalid product" in caplog.text
    assert len(caplog.records) == 3


def test_invalid_store_id_is_logged_and_dropped(caplog):
    df = pd.DataFrame(
        {
            "product_id": [1],
            "title": ["Product A"],
            "price": [9.99],
            "store_id": ["2|X|2"],
        }
    )

    result = validate_data(df, "products.csv")

    assert len(result) == 1
    assert len(result["store_id"]) == 1
    assert "Invalid store_id values" in caplog.text


def test_store_id_all_invalid_drops_row(caplog):
    df = pd.DataFrame(
        {
            "product_id": [1],
            "title": ["Product A"],
            "price": [9.99],
            "store_id": ["x|y"],
        }
    )

    result = validate_data(df, "products.csv")

    assert result.empty
    assert "store_id has no valid values" in caplog.text


def test_valid_dataframe_passes():
    expected = pd.DataFrame(
        {
            "product_id": [1, 2],
            "title": ["A", "B"],
            "price": [10.0, 20.0],
            "store_id": [[2, 4], [3]],
        }
    )

    df = pd.DataFrame(
        {
            "product_id": [1, 2],
            "title": ["A", "B"],
            "price": [10.0, 20.0],
            "store_id": ["2|4", "3"],
        }
    )
    result = validate_data(df, "whatever")
    assert result.equals(expected)
