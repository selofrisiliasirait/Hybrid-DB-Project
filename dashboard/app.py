import streamlit as st
import pandas as pd

from sqlalchemy import create_engine
from pymongo import MongoClient

# =========================
# AUTO REFRESH
# =========================

st.set_page_config(
    page_title="Hybrid E-Commerce Dashboard",
    layout="wide"
)

# Refresh sederhana setiap reload browser
# untuk proyek kampus sudah cukup memenuhi
# konsep dashboard membaca data terbaru

# =========================
# DATABASE CONNECTION
# =========================

engine = create_engine(
    "postgresql+psycopg2://postgres:selo150906selo@localhost:5432/olist_hybrid"
)

mongo_client = MongoClient(
    "mongodb://localhost:27017/"
)

mongo_db = mongo_client["olist_mongo"]

st.title("📊 Hybrid E-Commerce Dashboard")
st.caption("PostgreSQL + MongoDB")

try:

    # =========================
    # KPI
    # =========================

    revenue = pd.read_sql("""
    SELECT COALESCE(SUM(payment_value),0) AS total_revenue
    FROM payments;
    """, engine)

    orders = pd.read_sql("""
    SELECT COUNT(*) AS total_orders
    FROM orders;
    """, engine)

    customers = pd.read_sql("""
    SELECT COUNT(*) AS total_customers
    FROM customers;
    """, engine)

    avg_rating_result = list(
        mongo_db["reviews"].aggregate([
            {
                "$group": {
                    "_id": None,
                    "avg_rating": {
                        "$avg": "$review_score"
                    }
                }
            }
        ])
    )

    avg_rating = 0

    if len(avg_rating_result) > 0:
        avg_rating = round(
            avg_rating_result[0]["avg_rating"],
            2
        )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Revenue",
        f"R$ {revenue.iloc[0]['total_revenue']:,.2f}"
    )

    col2.metric(
        "Total Orders",
        f"{orders.iloc[0]['total_orders']:,}"
    )

    col3.metric(
        "Total Customers",
        f"{customers.iloc[0]['total_customers']:,}"
    )

    col4.metric(
        "Average Rating",
        f"{avg_rating} ⭐"
    )

    st.divider()

    # =========================
    # REVENUE TREND
    # =========================

    st.subheader("📈 Revenue Trend")

    revenue_trend = pd.read_sql("""
    SELECT
        DATE_TRUNC(
            'month',
            o.order_purchase_timestamp
        ) AS month,
        SUM(p.payment_value) AS revenue
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY month
    ORDER BY month
    """, engine)

    if not revenue_trend.empty:

        st.line_chart(
            revenue_trend.set_index("month")["revenue"]
        )

    st.divider()

    # =========================
    # 2 GRAFIK DALAM 2 KOLOM
    # =========================

    left, right = st.columns(2)

    with left:

        st.subheader("📦 Order Status")

        status_df = pd.read_sql("""
        SELECT
            order_status,
            COUNT(*) AS total
        FROM orders
        GROUP BY order_status
        ORDER BY total DESC
        """, engine)

        if not status_df.empty:

            st.bar_chart(
                status_df.set_index(
                    "order_status"
                )["total"]
            )

    with right:

        st.subheader("⭐ Review Distribution")

        review_df = pd.DataFrame(
            list(
                mongo_db["reviews"].find(
                    {},
                    {
                        "_id": 0,
                        "review_score": 1
                    }
                )
            )
        )

        if not review_df.empty:

            rating_distribution = (
                review_df
                .groupby("review_score")
                .size()
                .reset_index(name="count")
            )

            st.bar_chart(
                rating_distribution.set_index(
                    "review_score"
                )["count"]
            )

    st.divider()

    # =========================
    # TOP PRODUCT CATEGORY
    # =========================

    st.subheader("🏆 Top Product Categories")

    category_df = pd.read_sql("""
    SELECT
        p.product_category_name,
        COUNT(*) AS total_orders
    FROM products p
    JOIN order_items oi
        ON p.product_id = oi.product_id
    GROUP BY p.product_category_name
    ORDER BY total_orders DESC
    LIMIT 10
    """, engine)

    st.dataframe(
        category_df,
        use_container_width=True
    )

    st.divider()

    # =========================
    # TRANSAKSI TERBARU
    # =========================

    st.subheader("🧾 Recent Orders")

    recent_orders = pd.read_sql("""
    SELECT
        o.order_id,
        o.order_purchase_timestamp,
        o.order_status,
        COALESCE(
            SUM(p.payment_value),
            0
        ) AS payment_value
    FROM orders o
    LEFT JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY
        o.order_id,
        o.order_purchase_timestamp,
        o.order_status
    ORDER BY
        o.order_purchase_timestamp DESC
    LIMIT 20
    """, engine)

    st.dataframe(
        recent_orders,
        use_container_width=True
    )

    st.divider()

    # =========================
    # REVIEW TERBARU
    # =========================

    st.subheader("💬 Recent Reviews")

    recent_reviews = pd.DataFrame(
        list(
            mongo_db["reviews"].find(
                {},
                {
                    "_id": 0,
                    "review_score": 1,
                    "review_comment_title": 1,
                    "review_comment_message": 1
                }
            ).limit(20)
        )
    )

    if not recent_reviews.empty:

        st.dataframe(
            recent_reviews,
            use_container_width=True
        )

except Exception as e:

    st.error(
        f"Dashboard Error: {e}"
    )