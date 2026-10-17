# MongoDB Schema Documentation

## Database

```text
olist_mongo
```

MongoDB digunakan untuk menyimpan data yang lebih fleksibel (NoSQL Document Database) dan hasil analisis dari PostgreSQL.

---

# Collection: reviews

Sumber data:

```text
olist_order_reviews_dataset.csv
```

Tujuan:

Menyimpan review pelanggan terhadap pesanan yang telah dilakukan.

Contoh document:

```json
{
    "review_id": "7bc2406110b926393aa56f80a40eba40",
    "order_id": "73fc7af87114b39712e6da79b0a377eb",
    "review_score": 4,
    "review_comment_title": null,
    "review_comment_message": null,
    "review_creation_date": "2018-01-18",
    "review_answer_timestamp": "2018-01-18 21:46:00"
}
```

Field:

| Field | Type | Description |
|---------|---------|---------|
| review_id | String | ID review |
| order_id | String | ID order |
| review_score | Integer | Nilai rating 1-5 |
| review_comment_title | String | Judul review |
| review_comment_message | String | Isi review |
| review_creation_date | Date | Tanggal review dibuat |
| review_answer_timestamp | Date | Tanggal review dijawab |

---

# Collection: customer_purchase_history

Sumber data:

```text
Hasil transformasi PostgreSQL
```

Dibentuk dari:

```text
customers
JOIN orders
JOIN order_items
```

Tujuan:

Menyimpan riwayat pembelian customer dalam satu document.

Contoh document:

```json
{
    "customer_id": "06b8999e2fba1a1fbc88172c00ba8bc7",
    "orders": [
        {
            "order_id": "00010242fe8c5a6d1ba2dd792cb16214",
            "items": [
                {
                    "product_id": "4244733e06e7ecb4970a6e2683c13e61",
                    "price": 58.90
                }
            ]
        }
    ]
}
```

Field:

| Field | Type | Description |
|---------|---------|---------|
| customer_id | String | ID customer |
| orders | Array | Daftar order customer |
| orders.order_id | String | ID order |
| orders.items | Array | Daftar item dalam order |
| orders.items.product_id | String | Produk yang dibeli |
| orders.items.price | Decimal | Harga produk |

---

# Collection: product_analytics

Sumber data:

```text
Hasil agregasi PostgreSQL
```

Dibentuk dari:

```text
order_items
```

Tujuan:

Menyimpan data analitik per produk.

Contoh document:

```json
{
    "product_id": "4244733e06e7ecb4970a6e2683c13e61",
    "total_orders": 357,
    "total_sales": 15483.90
}
```

Field:

| Field | Type | Description |
|---------|---------|---------|
| product_id | String | ID produk |
| total_orders | Integer | Total pesanan |
| total_sales | Decimal | Total nilai penjualan |

---

# Hybrid Database Usage

## PostgreSQL

Digunakan untuk:

- customers
- orders
- products