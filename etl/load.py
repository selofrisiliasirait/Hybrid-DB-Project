# load.py

from sqlalchemy import create_engine, text
from pymongo import MongoClient
import pandas as pd

# ==========================
# KONFIGURASI DATABASE
# ==========================

POSTGRES_PASSWORD = "PASSWORD_POSTGRES_KAMU"

engine = create_engine(
    f"postgresql+psycopg2://postgres:selo150906selo@localhost:5432/olist_hybrid"
)

mongo_client = MongoClient(
    "mongodb://localhost:27017/"
)

mongo_db = mongo_client["olist_mongo"]


# ==========================
# RESET POSTGRESQL
# ==========================

def clear_postgresql_tables():

    with engine.begin() as conn:

        conn.execute(text("""
            TRUNCATE TABLE
                order_items,
                payments,
                orders,
                products,
                sellers,
                customers,
                geolocation
            RESTART IDENTITY
            CASCADE;
        """))

    print("[LOAD] PostgreSQL tables cleared")


# ==========================
# LOAD KE POSTGRESQL
# ==========================

def load_postgresql(data):

    clear_postgresql_tables()

    postgres_tables = [
        "customers",
        "products",
        "sellers",
        "orders",
        "payments",
        "order_items",
        "geolocation"
    ]

    for table in postgres_tables:

        print(f"[LOAD] PostgreSQL -> {table}")

        data[table].to_sql(
            table,
            engine,
            if_exists="append",
            index=False
        )


# ==========================
# LOAD REVIEW KE MONGODB
# ==========================

def load_reviews(data):

    collection = mongo_db["reviews"]

    collection.delete_many({})

    records = (
        data["reviews"]
        .where(pd.notnull(data["reviews"]), None)
        .to_dict("records")
    )

    collection.insert_many(records)

    print(
        f"[LOAD] reviews: {len(records)} docs"
    )


# ==========================
# CUSTOMER PURCHASE HISTORY
# ==========================
def create_customer_purchase_history():


    query = """
    SELECT
        c.customer_id,
        o.order_id,
        oi.product_id,
        oi.price
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN order_items oi
        ON o.order_id = oi.order_id
    """

    df = pd.read_sql(query, engine)

    collection = mongo_db["customer_purchase_history"]

    collection.delete_many({})

    result = {}

    for _, row in df.iterrows():

        customer_id = row["customer_id"]

        if customer_id not in result:
            result[customer_id] = {
                "customer_id": customer_id,
                "orders": {}
            }

        order_id = row["order_id"]

        if order_id not in result[customer_id]["orders"]:
            result[customer_id]["orders"][order_id] = {
                "order_id": order_id,
                "items": []
            }

        result[customer_id]["orders"][order_id]["items"].append({
            "product_id": row["product_id"],
            "price": float(row["price"])
        })

    documents = []

    for customer in result.values():

        customer["orders"] = list(
            customer["orders"].values()
        )

        documents.append(customer)

    collection.insert_many(documents)

    print(
        f"[MONGO] customer_purchase_history: {len(documents)} docs"
    )


# ==========================
# PRODUCT ANALYTICS
# ==========================

def create_product_analytics():

    query = """
    SELECT
        product_id,
        COUNT(*) AS total_orders,
        SUM(price) AS total_sales
    FROM order_items
    GROUP BY product_id
    """

    df = pd.read_sql(query, engine)

    collection = mongo_db["product_analytics"]

    collection.delete_many({})

    collection.insert_many(
        df.to_dict("records")
    )

    print(
        f"[MONGO] product_analytics: {len(df)} docs"
    )