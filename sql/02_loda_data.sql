/*============================================================
 RetailIQ Analytics Platform
 Day 13
 Raw Data Load
=============================================================*/

------------------------------------------------------------
-- USE OBJECTS
------------------------------------------------------------

USE WAREHOUSE RETAILIQ_WH;
USE DATABASE RETAILIQ_DB;
USE SCHEMA ANALYTICS;

------------------------------------------------------------
-- CREATE FILE FORMAT
------------------------------------------------------------

CREATE OR REPLACE FILE FORMAT CSV_FORMAT
TYPE = CSV
FIELD_DELIMITER = ','
SKIP_HEADER = 1
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
NULL_IF = ('NULL','')
EMPTY_FIELD_AS_NULL = TRUE;

------------------------------------------------------------
-- CREATE STAGE
------------------------------------------------------------

CREATE OR REPLACE STAGE RETAILIQ_STAGE
URL='s3://<YOUR_BUCKET_NAME>/'
FILE_FORMAT = CSV_FORMAT;

------------------------------------------------------------
-- DROP TABLES (OPTIONAL)
------------------------------------------------------------

DROP TABLE IF EXISTS CATEGORY_TRANSLATION;
DROP TABLE IF EXISTS CUSTOMERS;
DROP TABLE IF EXISTS GEOLOCATION;
DROP TABLE IF EXISTS ORDER_ITEMS;
DROP TABLE IF EXISTS ORDERS;
DROP TABLE IF EXISTS PAYMENTS;
DROP TABLE IF EXISTS PRODUCTS;
DROP TABLE IF EXISTS REVIEWS;
DROP TABLE IF EXISTS SELLERS;

------------------------------------------------------------
-- CREATE TABLES
------------------------------------------------------------

CREATE OR REPLACE TABLE CATEGORY_TRANSLATION (
    product_category_name STRING,
    product_category_name_english STRING
);

CREATE OR REPLACE TABLE CUSTOMERS (
    customer_id STRING,
    customer_unique_id STRING,
    customer_zip_code_prefix INTEGER,
    customer_city STRING,
    customer_state STRING
);

CREATE OR REPLACE TABLE GEOLOCATION (
    geolocation_zip_code_prefix INTEGER,
    geolocation_lat FLOAT,
    geolocation_lng FLOAT,
    geolocation_city STRING,
    geolocation_state STRING
);

CREATE OR REPLACE TABLE ORDER_ITEMS (
    order_id STRING,
    order_item_id INTEGER,
    product_id STRING,
    seller_id STRING,
    shipping_limit_date TIMESTAMP,
    price FLOAT,
    freight_value FLOAT
);

CREATE OR REPLACE TABLE ORDERS (
    order_id STRING,
    customer_id STRING,
    order_status STRING,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date DATE
);

CREATE OR REPLACE TABLE PAYMENTS (
    order_id STRING,
    payment_sequential INTEGER,
    payment_type STRING,
    payment_installments INTEGER,
    payment_value FLOAT
);

CREATE OR REPLACE TABLE PRODUCTS (
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

CREATE OR REPLACE TABLE REVIEWS (
    review_id STRING,
    order_id STRING,
    review_score INTEGER,
    review_comment_title STRING,
    review_comment_message STRING,
    review_creation_date DATE,
    review_answer_timestamp TIMESTAMP
);

CREATE OR REPLACE TABLE SELLERS (
    seller_id STRING,
    seller_zip_code_prefix INTEGER,
    seller_city STRING,
    seller_state STRING
);

------------------------------------------------------------
-- LOAD DATA
------------------------------------------------------------

COPY INTO CATEGORY_TRANSLATION
FROM @RETAILIQ_STAGE/category_translation_clean.csv;

COPY INTO CUSTOMERS
FROM @RETAILIQ_STAGE/customers_clean.csv;

COPY INTO GEOLOCATION
FROM @RETAILIQ_STAGE/geolocation_clean.csv;

COPY INTO ORDER_ITEMS
FROM @RETAILIQ_STAGE/order_items_clean.csv;

COPY INTO ORDERS
FROM @RETAILIQ_STAGE/orders_clean.csv;

COPY INTO PAYMENTS
FROM @RETAILIQ_STAGE/payments_clean.csv;

COPY INTO PRODUCTS
FROM @RETAILIQ_STAGE/products_clean.csv;

COPY INTO REVIEWS
FROM @RETAILIQ_STAGE/reviews_clean.csv;

COPY INTO SELLERS
FROM @RETAILIQ_STAGE/sellers_clean.csv;

------------------------------------------------------------
-- VALIDATION
------------------------------------------------------------

SELECT 'CATEGORY_TRANSLATION' AS table_name, COUNT(*) AS rows FROM CATEGORY_TRANSLATION
UNION ALL
SELECT 'CUSTOMERS', COUNT(*) FROM CUSTOMERS
UNION ALL
SELECT 'GEOLOCATION', COUNT(*) FROM GEOLOCATION
UNION ALL
SELECT 'ORDER_ITEMS', COUNT(*) FROM ORDER_ITEMS
UNION ALL
SELECT 'ORDERS', COUNT(*) FROM ORDERS
UNION ALL
SELECT 'PAYMENTS', COUNT(*) FROM PAYMENTS
UNION ALL
SELECT 'PRODUCTS', COUNT(*) FROM PRODUCTS
UNION ALL
SELECT 'REVIEWS', COUNT(*) FROM REVIEWS
UNION ALL
SELECT 'SELLERS', COUNT(*) FROM SELLERS;

------------------------------------------------------------
-- DATA QUALITY CHECKS
------------------------------------------------------------

-- Orders with NULL primary key
SELECT COUNT(*) AS null_order_ids
FROM ORDERS
WHERE order_id IS NULL;

-- Duplicate Orders
SELECT order_id, COUNT(*)
FROM ORDERS
GROUP BY order_id
HAVING COUNT(*) > 1;

-- Missing Products referenced by Order Items
SELECT COUNT(*) AS missing_products
FROM ORDER_ITEMS oi
LEFT JOIN PRODUCTS p
ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;

-- Orders without Order Items
SELECT COUNT(*) AS orders_without_items
FROM ORDERS o
LEFT JOIN ORDER_ITEMS oi
ON o.order_id = oi.order_id
WHERE oi.order_id IS NULL;