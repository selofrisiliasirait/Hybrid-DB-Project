# transform.py

import pandas as pd


def transform_data(data):

    print("[TRANSFORM] Cleaning data...")

    # Orders timestamps
    order_dates = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date"
    ]

    for col in order_dates:

        data["orders"][col] = pd.to_datetime(
            data["orders"][col],
            errors="coerce"
        )

    # Order items timestamp

    data["order_items"]["shipping_limit_date"] = pd.to_datetime(
        data["order_items"]["shipping_limit_date"],
        errors="coerce"
    )

    # Reviews timestamp

    if "review_creation_date" in data["reviews"].columns:

        data["reviews"]["review_creation_date"] = pd.to_datetime(
            data["reviews"]["review_creation_date"],
            errors="coerce"
        )

    if "review_answer_timestamp" in data["reviews"].columns:

        data["reviews"]["review_answer_timestamp"] = pd.to_datetime(
            data["reviews"]["review_answer_timestamp"],
            errors="coerce"
        )

    print("[TRANSFORM] Complete")

    return data