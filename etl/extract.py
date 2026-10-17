# extract.py

import pandas as pd
import os


def extract_data(dataset_path):

    data = {}

    files = {
        "customers": "olist_customers_dataset.csv",
        "products": "olist_products_dataset.csv",
        "sellers": "olist_sellers_dataset.csv",
        "orders": "olist_orders_dataset.csv",
        "payments": "olist_order_payments_dataset.csv",
        "order_items": "olist_order_items_dataset.csv",
        "geolocation": "olist_geolocation_dataset.csv",
        "reviews": "olist_order_reviews_dataset.csv"
    }

    for key, filename in files.items():

        file_path = os.path.join(dataset_path, filename)

        data[key] = pd.read_csv(file_path)

        print(
            f"[EXTRACT] {key}: {len(data[key])} rows"
        )

    return data