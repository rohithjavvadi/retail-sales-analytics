/*============================================================
 RetailIQ Analytics Platform
 Day 13
 Data Quality Validation
=============================================================*/

USE DATABASE RETAILIQ_DB;
USE SCHEMA ANALYTICS;

------------------------------------------------------------
-- 1. RAW TABLE ROW COUNTS
------------------------------------------------------------

SELECT 'CATEGORY_TRANSLATION' AS table_name, COUNT(*) AS total_rows FROM CATEGORY_TRANSLATION
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
-- 2. STAR SCHEMA ROW COUNTS
------------------------------------------------------------

SELECT 'DIM_CUSTOMERS' AS table_name, COUNT(*) AS total_rows FROM DIM_CUSTOMERS
UNION ALL
SELECT 'DIM_PRODUCTS', COUNT(*) FROM DIM_PRODUCTS
UNION ALL
SELECT 'DIM_SELLERS', COUNT(*) FROM DIM_SELLERS
UNION ALL
SELECT 'DIM_DATE', COUNT(*) FROM DIM_DATE
UNION ALL
SELECT 'FACT_SALES', COUNT(*) FROM FACT_SALES;

------------------------------------------------------------
-- 3. NULL PRIMARY KEY CHECKS
------------------------------------------------------------

SELECT COUNT(*) AS null_customer_ids
FROM CUSTOMERS
WHERE customer_id IS NULL;

SELECT COUNT(*) AS null_order_ids
FROM ORDERS
WHERE order_id IS NULL;

SELECT COUNT(*) AS null_product_ids
FROM PRODUCTS
WHERE product_id IS NULL;

SELECT COUNT(*) AS null_seller_ids
FROM SELLERS
WHERE seller_id IS NULL;

------------------------------------------------------------
-- 4. DUPLICATE BUSINESS KEY CHECKS
------------------------------------------------------------

SELECT customer_id, COUNT(*) AS duplicate_count
FROM CUSTOMERS
GROUP BY customer_id
HAVING COUNT(*) > 1;

SELECT order_id, COUNT(*) AS duplicate_count
FROM ORDERS
GROUP BY order_id
HAVING COUNT(*) > 1;

SELECT product_id, COUNT(*) AS duplicate_count
FROM PRODUCTS
GROUP BY product_id
HAVING COUNT(*) > 1;

SELECT seller_id, COUNT(*) AS duplicate_count
FROM SELLERS
GROUP BY seller_id
HAVING COUNT(*) > 1;

------------------------------------------------------------
-- 5. CATEGORY TRANSLATION DUPLICATES
------------------------------------------------------------

SELECT
    product_category_name,
    COUNT(*) AS duplicate_count
FROM CATEGORY_TRANSLATION
GROUP BY product_category_name
HAVING COUNT(*) > 1;

------------------------------------------------------------
-- 6. REFERENTIAL INTEGRITY CHECKS
------------------------------------------------------------

-- Order Items referencing missing Products

SELECT COUNT(*) AS missing_products
FROM ORDER_ITEMS oi
LEFT JOIN PRODUCTS p
ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;

------------------------------------------------------------

-- Order Items referencing missing Sellers

SELECT COUNT(*) AS missing_sellers
FROM ORDER_ITEMS oi
LEFT JOIN SELLERS s
ON oi.seller_id = s.seller_id
WHERE s.seller_id IS NULL;

------------------------------------------------------------

-- Orders referencing missing Customers

SELECT COUNT(*) AS missing_customers
FROM ORDERS o
LEFT JOIN CUSTOMERS c
ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

------------------------------------------------------------
-- 7. ORDERS WITHOUT ITEMS
------------------------------------------------------------

SELECT COUNT(*) AS orders_without_items
FROM ORDERS o
LEFT JOIN ORDER_ITEMS oi
ON o.order_id = oi.order_id
WHERE oi.order_id IS NULL;

------------------------------------------------------------
-- 8. FACT TABLE VALIDATION
------------------------------------------------------------

SELECT COUNT(*) AS fact_rows
FROM FACT_SALES;

SELECT COUNT(DISTINCT order_id) AS distinct_orders
FROM FACT_SALES;

------------------------------------------------------------
-- 9. BUSINESS METRICS
------------------------------------------------------------

SELECT
    ROUND(SUM(price),2) AS total_sales,
    ROUND(SUM(freight_value),2) AS total_freight,
    ROUND(SUM(payment_value),2) AS total_payment
FROM FACT_SALES;

------------------------------------------------------------
-- 10. UNKNOWN PRODUCT VALIDATION
------------------------------------------------------------

SELECT COUNT(*) AS unknown_product_rows
FROM FACT_SALES
WHERE product_key = 0;

------------------------------------------------------------
-- 11. DATE DIMENSION VALIDATION
------------------------------------------------------------

SELECT
    MIN(full_date) AS first_date,
    MAX(full_date) AS last_date,
    COUNT(*) AS total_dates
FROM DIM_DATE;

------------------------------------------------------------
-- 12. FINAL SUMMARY
------------------------------------------------------------

SELECT
    'Warehouse Validation Completed Successfully' AS status;