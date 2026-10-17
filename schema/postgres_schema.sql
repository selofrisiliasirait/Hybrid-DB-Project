\c olist_hybrid

-- =========================================================
-- RESET (urutan: tabel anak dulu, baru tabel induk)
-- =========================================================
DROP TABLE IF EXISTS order_reviews CASCADE;
DROP TABLE IF EXISTS order_items CASCADE;
DROP TABLE IF EXISTS payments CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS geolocation CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS sellers CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS product_category_name_translation CASCADE;

-- =========================================================
-- TABEL MASTER
-- =========================================================
CREATE TABLE customers (
    customer_id               VARCHAR(50) PRIMARY KEY,
    customer_unique_id        VARCHAR(50),
    customer_zip_code_prefix  INT,
    customer_city             VARCHAR(100),
    customer_state            VARCHAR(10)
);

CREATE TABLE products (
    product_id                  VARCHAR(50) PRIMARY KEY,
    product_category_name       VARCHAR(100),
    product_name_lenght         INT,
    product_description_lenght  INT,
    product_photos_qty          INT,
    product_weight_g            INT,
    product_length_cm           INT,
    product_height_cm           INT,
    product_width_cm            INT
);

CREATE TABLE sellers (
    seller_id               VARCHAR(50) PRIMARY KEY,
    seller_zip_code_prefix  INT,
    seller_city             VARCHAR(100),
    seller_state            VARCHAR(10)
);

CREATE TABLE product_category_name_translation (
    product_category_name          VARCHAR(100) PRIMARY KEY,
    product_category_name_english  VARCHAR(100)
);

-- Tanpa PK karena zip code prefix berulang di dataset asli
CREATE TABLE geolocation (
    geolocation_zip_code_prefix  INT,
    geolocation_lat              NUMERIC(12,8),
    geolocation_lng              NUMERIC(12,8),
    geolocation_city             VARCHAR(100),
    geolocation_state            VARCHAR(10)
);

-- =========================================================
-- TABEL TRANSAKSI
-- =========================================================
CREATE TABLE orders (
    order_id                       VARCHAR(50) PRIMARY KEY,
    customer_id                    VARCHAR(50),
    order_status                   VARCHAR(50),
    order_purchase_timestamp       TIMESTAMP,
    order_approved_at              TIMESTAMP,
    order_delivered_carrier_date   TIMESTAMP,
    order_delivered_customer_date  TIMESTAMP,
    order_estimated_delivery_date  TIMESTAMP,

    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE payments (
    order_id              VARCHAR(50),
    payment_sequential    INT,
    payment_type          VARCHAR(50),
    payment_installments  INT,
    payment_value         NUMERIC(10,2),

    PRIMARY KEY (order_id, payment_sequential),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE order_items (
    order_id             VARCHAR(50),
    order_item_id        INT,
    product_id           VARCHAR(50),
    seller_id            VARCHAR(50),
    shipping_limit_date  TIMESTAMP,
    price                NUMERIC(10,2),
    freight_value        NUMERIC(10,2),

    PRIMARY KEY (order_id, order_item_id),
    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    FOREIGN KEY (seller_id)  REFERENCES sellers(seller_id)
);

-- review_id di data asli tidak unik, jadi PK-nya gabungan
CREATE TABLE order_reviews (
    review_id                VARCHAR(50),
    order_id                 VARCHAR(50),
    review_score             INT,
    review_comment_title     TEXT,
    review_comment_message   TEXT,
    review_creation_date     TIMESTAMP,
    review_answer_timestamp  TIMESTAMP,

    PRIMARY KEY (review_id, order_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

-- =========================================================
-- INDEX UNTUK MEMPERCEPAT JOIN / QUERY
-- =========================================================
CREATE INDEX idx_orders_customer     ON orders(customer_id);
CREATE INDEX idx_orders_status       ON orders(order_status);
CREATE INDEX idx_orders_purchase     ON orders(order_purchase_timestamp);
CREATE INDEX idx_items_product       ON order_items(product_id);
CREATE INDEX idx_items_seller        ON order_items(seller_id);
CREATE INDEX idx_reviews_order       ON order_reviews(order_id);
CREATE INDEX idx_customers_zip       ON customers(customer_zip_code_prefix);
CREATE INDEX idx_sellers_zip         ON sellers(seller_zip_code_prefix);
CREATE INDEX idx_geo_zip             ON geolocation(geolocation_zip_code_prefix);
CREATE INDEX idx_products_category   ON products(product_category_name);

-- Cek hasil
\dt