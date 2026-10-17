
from extract import extract_data
from transform import transform_data

from load import (
    load_postgresql,
    load_reviews,
    create_customer_purchase_history,
    create_product_analytics
)

import os

BASE_DIR = os.path.dirname(__file__)

DATASET_PATH = os.path.join(
    BASE_DIR,
    "..",
    "dataset"
)

print("============")
print("ETL PIPELINE")
print("============")

data = extract_data(DATASET_PATH)

data = transform_data(data)

load_postgresql(data)

load_reviews(data)

create_customer_purchase_history()

create_product_analytics()

print()
print("PIPELINE SELESAI")

try:

    data = extract_data(DATASET_PATH)

    data = transform_data(data)

    load_postgresql(data)

    load_reviews(data)

    create_customer_purchase_history()

    create_product_analytics()

    print("\nPIPELINE SELESAI")

except Exception as e:

    print(f"ERROR: {e}")