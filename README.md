Hybrid Database Architecture & Automated ETL Project
Overview

Proyek ini merupakan implementasi Hybrid Database Architecture dan Automated ETL Pipeline menggunakan:

PostgreSQL (Relational Database)
MongoDB (NoSQL Document Database)
Python ETL Pipeline
Streamlit Dashboard

Dataset yang digunakan adalah Olist Brazilian E-Commerce Dataset.

Proyek ini memenuhi requirement:

Polyglot Database Architecture
Automated ETL Pipeline
Real-time Dashboard
Database Integration
Data Transformation
Data Analytics
Project Architecture
               +----------------+
               | CSV Datasets   |
               +--------+-------+
                        |
                        |
                        v
               +----------------+
               | Extract Module |
               +----------------+
                        |
                        v
               +----------------+
               | Transform      |
               | Module         |
               +----------------+
                        |
                        v
               +----------------+
               | Load Module    |
               +-------+--------+
                       |
           +-----------+-----------+
           |                       |
           v                       v

    +-------------+       +----------------+
    | PostgreSQL  |       | MongoDB        |
    +-------------+       +----------------+
           |                     |
           +----------+----------+
                      |
                      v

            +--------------------+
            | Streamlit Dashboard|
            +--------------------+

Dataset

Semua dataset disimpan di:

dataset/


Isi dataset:

olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv

Technologies Used
PostgreSQL

Digunakan untuk data terstruktur:

customers
orders
products
sellers
payments
order_items
geolocation
MongoDB

Digunakan untuk data semi-structured dan analytical document:

reviews
customer_purchase_history
product_analytics
Python

Digunakan untuk:

ETL Process
Data Cleansing
Data Transformation
Database Integration
Streamlit

Digunakan untuk dashboard.

Project Structure
Hybrid-DB-Project
│
├── dataset/
│
├── etl/
│   ├── extract.py
│   ├── transform.py
│   ├── load.py
│   └── run_pipeline.py
│
├── dashboard/
│   └── app.py
│
├── docs/
│
├── schema/
│
├── backup/
│
└── README.md

Database Design
PostgreSQL Tables
customers
customer_id (PK)
customer_unique_id
customer_zip_code_prefix
customer_city
customer_state

orders
order_id (PK)
customer_id (FK)
order_status
order_purchase_timestamp
order_approved_at
order_delivered_carrier_date
order_delivered_customer_date
order_estimated_delivery_date

products
product_id (PK)
product_category_name
product_name_lenght
product_description_lenght
product_photos_qty
product_weight_g
product_length_cm
product_height_cm
product_width_cm

sellers
seller_id (PK)
seller_zip_code_prefix
seller_city
seller_state

payments
order_id (FK)
payment_sequential
payment_type
payment_installments
payment_value

order_items
order_id (FK)
order_item_id
product_id (FK)
seller_id (FK)
shipping_limit_date
price
freight_value

geolocation
geolocation_zip_code_prefix
geolocation_lat
geolocation_lng
geolocation_city
geolocation_state

Database Relationship
customers
    |
    |
orders
    |
    |
order_items
   / \
  /   \
products sellers

orders
   |
payments

MongoDB Collections
reviews

Berisi review pelanggan.

Contoh:

{
  "review_id": "...",
  "order_id": "...",
  "review_score": 5,
  "review_comment_title": "...",
  "review_comment_message": "..."
}

customer_purchase_history

Dibentuk dari data PostgreSQL.

Contoh:

{
  "customer_id": "...",
  "orders": [
    {
      "order_id": "...",
      "items": [
        {
          "product_id": "...",
          "price": 58.90
        }
      ]
    }
  ]
}

product_analytics

Dibentuk dari data PostgreSQL.

Contoh:

{
  "product_id": "...",
  "total_orders": 25,
  "total_sales": 1500.50
}

ETL Pipeline
Extract

Dilakukan oleh:

extract.py


Tugas:

Membaca seluruh file CSV
Mengubahnya menjadi DataFrame
Menyiapkan data untuk proses transformasi
Transform

Dilakukan oleh:

transform.py


Tugas:

Mengubah format tanggal
Membersihkan data
Menyesuaikan format data sebelum dimasukkan ke database

Contoh:

pd.to_datetime()

Load

Dilakukan oleh:

load.py


Tugas:

Menghapus data lama
Memasukkan data ke PostgreSQL
Memasukkan review ke MongoDB
Membuat customer_purchase_history
Membuat product_analytics
Run Pipeline

Dilakukan oleh:

run_pipeline.py


Pipeline lengkap:

CSV
 ↓
EXTRACT
 ↓
TRANSFORM
 ↓
POSTGRESQL
 ↓
MONGODB
 ↓
ANALYTICS

Running ETL

Menjalankan seluruh ETL:

python etl/run_pipeline.py


Output:

[EXTRACT] customers
[EXTRACT] products
[EXTRACT] sellers
...

[TRANSFORM] Cleaning data

[LOAD] PostgreSQL

[LOAD] reviews

[MONGO] customer_purchase_history

[MONGO] product_analytics

PIPELINE SELESAI

Dashboard

Dashboard dibuat menggunakan Streamlit.

File:

dashboard/app.py


Menampilkan:

KPI
Total Revenue
Total Orders
Total Customers
Average Rating
Charts
Revenue Trend
Order Status Distribution
Review Distribution
Tables
Top Product Categories
Recent Orders
Recent Reviews
Running Dashboard

Jalankan:

streamlit run dashboard/app.py


Browser akan terbuka otomatis.

Real-Time Concept

Dashboard membaca data langsung dari:

PostgreSQL
MongoDB


Setelah ETL dijalankan:

python etl/run_pipeline.py


dashboard akan menampilkan data terbaru setelah refresh.

Automated ETL Concept

Automasi ETL dilakukan melalui:

run_pipeline.py


yang menjalankan seluruh proses:

Extract
Transform
Load PostgreSQL
Load MongoDB
Generate Analytics

dengan satu perintah.

Testing Performed
PostgreSQL

Verifikasi jumlah data:

SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM orders;
SELECT COUNT(*) FROM products;
SELECT COUNT(*) FROM sellers;
SELECT COUNT(*) FROM payments;
SELECT COUNT(*) FROM order_items;
SELECT COUNT(*) FROM geolocation;

MongoDB

Memastikan collection:

reviews
customer_purchase_history
product_analytics


berhasil dibuat.

Dashboard
KPI tampil
Grafik tampil
Data terhubung ke PostgreSQL
Data terhubung ke MongoDB
Contributors Responsibilities
Database Engineer A
Schema PostgreSQL
Relational Database Design
Database Engineer B
MongoDB Design
Collection Design
ETL Developer
Extract
Transform
Load
Pipeline Integration
Dashboard Developer
Streamlit Dashboard
KPI
Visualization
Documentation
README
Technical Report
Presentation
Conclusion

Proyek ini berhasil mengimplementasikan:

✅ Hybrid Database Architecture
 ✅ PostgreSQL Integration
 ✅ MongoDB Integration
 ✅ Automated ETL Pipeline
 ✅ Data Transformation
 ✅ Analytics Generation
 ✅ Real-Time Dashboard
 ✅ Database Visualization

dan memenuhi requirement utama tugas Capstone Project: Hybrid Database Architecture & ETL.