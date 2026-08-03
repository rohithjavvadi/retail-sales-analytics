/*
===========================================================
RetailIQ Analytics Platform
Day 12 - Snowflake Data Warehouse Setup
Author: Rohith Javvadi
Description:
    Creates the Snowflake warehouse, database, schema,
    file format, stage, tables, and loads the cleaned
    Olist datasets into Snowflake.
===========================================================
*/

-----------------------------------------------------------
-- 1. CREATE WAREHOUSE
-----------------------------------------------------------

CREATE OR REPLACE WAREHOUSE RETAILIQ_WH
WITH
WAREHOUSE_SIZE = 'XSMALL'
AUTO_SUSPEND = 60
AUTO_RESUME = TRUE
INITIALLY_SUSPENDED = TRUE;

USE WAREHOUSE RETAILIQ_WH;

-----------------------------------------------------------
-- 2. CREATE DATABASE
-----------------------------------------------------------

CREATE OR REPLACE DATABASE RETAILIQ_DB;

USE DATABASE RETAILIQ_DB;

-----------------------------------------------------------
-- 3. CREATE SCHEMA
-----------------------------------------------------------

CREATE OR REPLACE SCHEMA ANALYTICS;

USE SCHEMA ANALYTICS;

-----------------------------------------------------------
-- 4. CREATE FILE FORMAT
-----------------------------------------------------------

CREATE OR REPLACE FILE FORMAT csv_format
TYPE = CSV
FIELD_DELIMITER = ','
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
NULL_IF = ('NULL','null','');

-----------------------------------------------------------
-- 5. CREATE INTERNAL STAGE
-----------------------------------------------------------

CREATE OR REPLACE STAGE retailiq_stage
FILE_FORMAT = csv_format;

-----------------------------------------------------------
-- 6. CREATE TABLES
-----------------------------------------------------------

CREATE OR REPLACE TABLE customers
(
    customer_id STRING,
    customer_unique_id STRING,
    customer_zip_code_prefix INTEGER,
    customer_city STRING,
    customer_state STRING
);

CREATE OR REPLACE TABLE orders
(
    order_id STRING,
    customer_id STRING,
    order_status STRING,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);

CREATE OR REPLACE TABLE order_items
(
    order_id STRING,
    order_item_id INTEGER,
    product_id STRING,
    seller_id STRING,
    shipping_limit_date TIMESTAMP,
    price FLOAT,
    freight_value FLOAT
);

CREATE OR REPLACE TABLE products
(
    product_id STRING,
    product_category_name STRING,
    product_name_length INTEGER,
    product_description_length INTEGER,
    product_photos_qty INTEGER,
    product_weight_g FLOAT,
    product_length_cm FLOAT,
    product_height_cm FLOAT,
    product_width_cm FLOAT
);

CREATE OR REPLACE TABLE sellers
(
    seller_id STRING,
    seller_zip_code_prefix INTEGER,
    seller_city STRING,
    seller_state STRING
);

CREATE OR REPLACE TABLE payments
(
    order_id STRING,
    payment_sequential INTEGER,
    payment_type STRING,
    payment_installments INTEGER,
    payment_value FLOAT
);

CREATE OR REPLACE TABLE reviews
(
    review_id STRING,
    order_id STRING,
    review_score INTEGER,
    review_comment_title STRING,
    review_comment_message STRING,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);

CREATE OR REPLACE TABLE geolocation
(
    geolocation_zip_code_prefix INTEGER,
    geolocation_lat FLOAT,
    geolocation_lng FLOAT,
    geolocation_city STRING,
    geolocation_state STRING
);

CREATE OR REPLACE TABLE category_translation
(
    product_category_name STRING,
    product_category_name_english STRING
);

-----------------------------------------------------------
-- 7. LOAD DATA
-----------------------------------------------------------

COPY INTO customers
FROM @retailiq_stage/customers_clean.csv
FILE_FORMAT = (FORMAT_NAME = csv_format)
FORCE = TRUE;

COPY INTO orders
FROM @retailiq_stage/orders_clean.csv
FILE_FORMAT = (FORMAT_NAME = csv_format)
FORCE = TRUE;

COPY INTO order_items
FROM @retailiq_stage/order_items_clean.csv
FILE_FORMAT = (FORMAT_NAME = csv_format)
FORCE = TRUE;

COPY INTO products
FROM @retailiq_stage/products_clean.csv
FILE_FORMAT = (FORMAT_NAME = csv_format)
FORCE = TRUE;

COPY INTO sellers
FROM @retailiq_stage/sellers_clean.csv
FILE_FORMAT = (FORMAT_NAME = csv_format)
FORCE = TRUE;

COPY INTO payments
FROM @retailiq_stage/payments_clean.csv
FILE_FORMAT = (FORMAT_NAME = csv_format)
FORCE = TRUE;

COPY INTO reviews
FROM @retailiq_stage/reviews_clean.csv
FILE_FORMAT = (FORMAT_NAME = csv_format)
FORCE = TRUE;

COPY INTO geolocation
FROM @retailiq_stage/geolocation_clean.csv
FILE_FORMAT = (FORMAT_NAME = csv_format)
FORCE = TRUE;

COPY INTO category_translation
FROM @retailiq_stage/category_translation_clean.csv
FILE_FORMAT = (FORMAT_NAME = csv_format)
FORCE = TRUE;

-----------------------------------------------------------
-- 8. VALIDATION
-----------------------------------------------------------

SHOW WAREHOUSES;

SHOW DATABASES;

SHOW SCHEMAS;

SHOW TABLES;

SHOW STAGES;

-----------------------------------------------------------
-- ROW COUNTS
-----------------------------------------------------------

SELECT 'customers' AS table_name, COUNT(*) AS row_count
FROM customers

UNION ALL

SELECT 'orders', COUNT(*)
FROM orders

UNION ALL

SELECT 'order_items', COUNT(*)
FROM order_items

UNION ALL

SELECT 'products', COUNT(*)
FROM products

UNION ALL

SELECT 'payments', COUNT(*)
FROM payments

UNION ALL

SELECT 'reviews', COUNT(*)
FROM reviews

UNION ALL

SELECT 'sellers', COUNT(*)
FROM sellers

UNION ALL

SELECT 'geolocation', COUNT(*)
FROM geolocation

UNION ALL

SELECT 'category_translation', COUNT(*)
FROM category_translation;

-----------------------------------------------------------
-- SAMPLE DATA
-----------------------------------------------------------

SELECT *
FROM customers
LIMIT 10;

SELECT *
FROM orders
LIMIT 10;

SELECT *
FROM products
LIMIT 10;