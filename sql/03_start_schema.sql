/*============================================================
  RetailIQ Analytics Platform
  Day 13 - Star Schema
=============================================================*/

USE DATABASE RETAILIQ_DB;
USE SCHEMA ANALYTICS;

------------------------------------------------------------
-- Clean Lookup Table
------------------------------------------------------------

CREATE OR REPLACE TABLE CATEGORY_TRANSLATION AS
SELECT DISTINCT
    product_category_name,
    product_category_name_english
FROM CATEGORY_TRANSLATION;

------------------------------------------------------------
-- DIM_CUSTOMERS
------------------------------------------------------------

CREATE OR REPLACE TABLE DIM_CUSTOMERS (
    customer_key INTEGER AUTOINCREMENT START 1 INCREMENT 1,
    customer_id STRING,
    customer_zip_code_prefix INTEGER,
    customer_city STRING,
    customer_state STRING
);

INSERT INTO DIM_CUSTOMERS (
    customer_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
)
SELECT DISTINCT
    customer_id,
    customer_zip_code_prefix,
    customer_city,
    customer_state
FROM CUSTOMERS;

------------------------------------------------------------
-- DIM_PRODUCTS
------------------------------------------------------------

CREATE OR REPLACE TABLE DIM_PRODUCTS (
    product_key INTEGER AUTOINCREMENT START 1 INCREMENT 1,
    product_id STRING,
    product_category_name STRING,
    product_category_name_english STRING,
    product_name_length INTEGER,
    product_description_length INTEGER,
    product_photos_qty INTEGER,
    product_weight_g FLOAT,
    product_length_cm FLOAT,
    product_height_cm FLOAT,
    product_width_cm FLOAT
);

INSERT INTO DIM_PRODUCTS (
    product_id,
    product_category_name,
    product_category_name_english,
    product_name_length,
    product_description_length,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
)
SELECT
    p.product_id,
    p.product_category_name,
    ct.product_category_name_english,
    p.product_name_length,
    p.product_description_length,
    p.product_photos_qty,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm
FROM PRODUCTS p
LEFT JOIN CATEGORY_TRANSLATION ct
ON p.product_category_name = ct.product_category_name;

------------------------------------------------------------
-- Unknown Product Member
------------------------------------------------------------

INSERT INTO DIM_PRODUCTS (
    product_key,
    product_id,
    product_category_name,
    product_category_name_english,
    product_name_length,
    product_description_length,
    product_photos_qty,
    product_weight_g,
    product_length_cm,
    product_height_cm,
    product_width_cm
)
VALUES (
    0,
    'UNKNOWN',
    'Unknown',
    'Unknown',
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL,
    NULL
);

------------------------------------------------------------
-- DIM_SELLERS
------------------------------------------------------------

CREATE OR REPLACE TABLE DIM_SELLERS (
    seller_key INTEGER AUTOINCREMENT START 1 INCREMENT 1,
    seller_id STRING,
    seller_zip_code_prefix INTEGER,
    seller_city STRING,
    seller_state STRING
);

INSERT INTO DIM_SELLERS (
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
)
SELECT DISTINCT
    seller_id,
    seller_zip_code_prefix,
    seller_city,
    seller_state
FROM SELLERS;

------------------------------------------------------------
-- DIM_DATE
------------------------------------------------------------

CREATE OR REPLACE TABLE DIM_DATE (
    date_key INTEGER PRIMARY KEY,
    full_date DATE,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name STRING,
    week INTEGER,
    day INTEGER,
    day_name STRING,
    is_weekend BOOLEAN
);

INSERT INTO DIM_DATE
SELECT
    TO_NUMBER(TO_CHAR(date_value,'YYYYMMDD')) AS date_key,
    date_value,
    YEAR(date_value),
    QUARTER(date_value),
    MONTH(date_value),
    MONTHNAME(date_value),
    WEEK(date_value),
    DAY(date_value),
    DAYNAME(date_value),
    CASE
        WHEN DAYOFWEEK(date_value) IN (1,7) THEN TRUE
        ELSE FALSE
    END
FROM (
    SELECT DATEADD(
        DAY,
        ROW_NUMBER() OVER (ORDER BY SEQ4())-1,
        '2016-01-01'
    ) AS date_value
    FROM TABLE(GENERATOR(ROWCOUNT=>1096))
);

------------------------------------------------------------
-- FACT_SALES
------------------------------------------------------------

CREATE OR REPLACE TABLE FACT_SALES AS

WITH PAYMENT_SUMMARY AS
(
    SELECT
        order_id,
        SUM(payment_value) AS payment_value
    FROM PAYMENTS
    GROUP BY order_id
)

SELECT

    oi.order_id,
    oi.order_item_id,

    dc.customer_key,

    COALESCE(dp.product_key,0) AS product_key,

    ds.seller_key,

    dd.date_key,

    oi.price,

    oi.freight_value,

    COALESCE(ps.payment_value,0) AS payment_value

FROM ORDER_ITEMS oi

JOIN ORDERS o
ON oi.order_id = o.order_id

LEFT JOIN PAYMENT_SUMMARY ps
ON oi.order_id = ps.order_id

JOIN DIM_CUSTOMERS dc
ON o.customer_id = dc.customer_id

LEFT JOIN DIM_PRODUCTS dp
ON oi.product_id = dp.product_id

JOIN DIM_SELLERS ds
ON oi.seller_id = ds.seller_id

JOIN DIM_DATE dd
ON CAST(o.order_purchase_timestamp AS DATE)=dd.full_date;

------------------------------------------------------------
-- VALIDATION
------------------------------------------------------------

SELECT 'DIM_CUSTOMERS' AS table_name, COUNT(*) FROM DIM_CUSTOMERS
UNION ALL
SELECT 'DIM_PRODUCTS', COUNT(*) FROM DIM_PRODUCTS
UNION ALL
SELECT 'DIM_SELLERS', COUNT(*) FROM DIM_SELLERS
UNION ALL
SELECT 'DIM_DATE', COUNT(*) FROM DIM_DATE
UNION ALL
SELECT 'FACT_SALES', COUNT(*) FROM FACT_SALES;

------------------------------------------------------------
-- BUSINESS VALIDATION
------------------------------------------------------------

SELECT COUNT(DISTINCT order_id) AS orders_in_fact
FROM FACT_SALES;

SELECT
    SUM(price) AS total_sales,
    SUM(freight_value) AS total_freight,
    SUM(payment_value) AS total_payments
FROM FACT_SALES;