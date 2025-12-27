import pandas as pd
import logging


logger = logging.getLogger(__name__)

COLUMNS = ("product_id", "name", "price", "store_id")


def validate_products(df, csv):
    missing = set(COLUMNS) - set(df.columns)
    if missing:
        raise KeyError(f"Missing columns: {missing}")
    df = df[list(COLUMNS)]

    valid_products = []

    for idx, product in df.iterrows():
        errors = []

        product_id = pd.to_numeric(product["product_id"], errors="coerce")
        if pd.isna(product_id):
            errors.append("product_id is invalid")

        if pd.isna(product["name"]):
            errors.append("name is null")

        price = pd.to_numeric(product["price"], errors="coerce")
        if pd.isna(price) or price < 0:
            errors.append("price is invalid")

        raw_store_id = product["store_id"]
        if pd.isna(raw_store_id):
            errors.append("store_id is null")
        else:
            ids = str(raw_store_id).split("|")

            valid_store_ids = {int(id) for id in ids if id.isdigit()}
            invalid_store_ids = [id for id in ids if not id.isdigit()]

        if invalid_store_ids:
            logger.error(
                "Invalid store_id values at row %s in CSV %s (product_id=%s): %s",  # noqa: E501
                idx,
                csv,
                product["product_id"],
                ", ".join(invalid_store_ids),
            )

        if not valid_store_ids:
            errors.append("store_id has no valid values")

        if errors:
            logger.error(
                "Invalid product at row %s in CSV %s (product_id=%s): %s",
                idx,
                csv,
                product["product_id"],
                ", ".join(errors),
            )
        else:
            valid_products.append(
                {
                    "product_id": int(product_id),
                    "name": str(product["name"]),
                    "price": float(price),
                    "store_id": list(valid_store_ids),
                }
            )

    return pd.DataFrame(valid_products)
