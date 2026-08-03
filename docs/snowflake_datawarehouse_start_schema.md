# Day 13 – Snowflake Data Warehouse & Star Schema

## Objective

The objective of Day 13 was to transform the cleaned RetailIQ datasets into a production-style analytics warehouse using Snowflake. Instead of querying normalized operational tables directly, we designed a dimensional model (Star Schema) that is optimized for analytics, reporting, and Power BI.

---

# Initial Dataset

The following cleaned datasets were successfully loaded into Snowflake:

* CUSTOMERS
* ORDERS
* ORDER_ITEMS
* PAYMENTS
* PRODUCTS
* SELLERS
* REVIEWS
* GEOLOCATION
* CATEGORY_TRANSLATION

All datasets were stored in the **ANALYTICS** schema.

---

# Data Validation

Before creating the warehouse, several validation checks were performed.

### Row Count Validation

| Table                |                  Rows |
| -------------------- | --------------------: |
| CUSTOMERS            |                99,441 |
| ORDERS               |                99,441 |
| ORDER_ITEMS          |               112,650 |
| PAYMENTS             |               103,886 |
| PRODUCTS             |                32,340 |
| SELLERS              |                 3,095 |
| REVIEWS              |                99,224 |
| GEOLOCATION          |             1,476,664 |
| CATEGORY_TRANSLATION | 213 (before cleaning) |

---

# Issue 1 – Duplicate Lookup Records

## Problem

While building `DIM_PRODUCTS`, the dimension contained **96,994** rows instead of **32,340**.

## Root Cause

The `CATEGORY_TRANSLATION` table contained duplicate records.

Example:

```text
beleza_saude                    3
esporte_lazer                   3
informatica_acessorios          3
```

Each product matched three translation records, causing the join to multiply rows.

## Solution

The lookup table was cleaned using `SELECT DISTINCT`, reducing the translation table from **213** rows to **71** unique category mappings.

After rebuilding the dimension:

* DIM_PRODUCTS = **32,340** rows

---

# Dimension Tables Created

## DIM_CUSTOMERS

Stores customer descriptive information.

Columns:

* customer_key
* customer_id
* customer_city
* customer_state
* customer_zip_code_prefix

Rows:

**99,441**

---

## DIM_PRODUCTS

Stores product attributes and English category names.

Columns include:

* product_key
* product_id
* product_category_name
* product_category_name_english
* weight
* dimensions
* description length
* photo count

Rows:

**32,340**

An additional **Unknown Product** member was later added for missing product references.

---

## DIM_SELLERS

Stores seller information.

Columns:

* seller_key
* seller_id
* seller_city
* seller_state
* seller_zip_code_prefix

Rows:

**3,095**

---

## DIM_DATE

Calendar dimension generated for all dates between 2016 and 2018.

Attributes include:

* date_key
* full_date
* year
* quarter
* month
* month_name
* week
* day
* day_name
* is_weekend

Rows:

**1,096**

---

# Fact Table

## FACT_SALES

### Grain

One row represents **one order item sold**.

This grain was selected because an order can contain multiple products.

Measures:

* price
* freight_value
* payment_value

Foreign Keys:

* customer_key
* product_key
* seller_key
* date_key

---

# Issue 2 – Duplicate Payments

Some orders contained multiple payment records.

Joining `PAYMENTS` directly would duplicate sales rows.

## Solution

Payments were aggregated by `order_id` before joining.

```sql
SELECT
    order_id,
    SUM(payment_value)
FROM PAYMENTS
GROUP BY order_id;
```

---

# Issue 3 – Missing Products

While building the fact table, only **111,046** rows were created instead of **112,650**.

## Investigation

Validation queries showed:

* Missing customers = 0
* Missing sellers = 0
* Missing dates = 0
* Missing products = 1,604

Some order items referenced products that did not exist in the PRODUCTS table.

## Solution

Implemented the Kimball "Unknown Member" pattern.

* Added an Unknown Product row to DIM_PRODUCTS.
* Used a LEFT JOIN and `COALESCE(product_key, 0)`.

Result:

FACT_SALES contained all **112,650** order items.

---

# Final Validation

| Object        |                               Rows |
| ------------- | ---------------------------------: |
| DIM_CUSTOMERS |                             99,441 |
| DIM_PRODUCTS  | 32,341 (including Unknown Product) |
| DIM_SELLERS   |                              3,095 |
| DIM_DATE      |                              1,096 |
| FACT_SALES    |                            112,650 |

Additional validation:

* Total Orders = **99,441**
* Orders without Order Items = **775**
* Orders represented in FACT_SALES = **98,666**

This confirms that the fact table correctly represents only orders containing purchased items.

---

# Final Star Schema

```text
                   DIM_CUSTOMERS
                         |
                         |
DIM_PRODUCTS ---- FACT_SALES ---- DIM_SELLERS
                         |
                         |
                     DIM_DATE
```

---

# Key Learnings

* Designed a dimensional model using the Kimball Star Schema approach.
* Created surrogate keys for all dimensions.
* Performed data quality validation before loading dimensions.
* Identified and resolved duplicate lookup records.
* Prevented fact table duplication by aggregating payments.
* Implemented an Unknown Dimension Member to preserve referential integrity.
* Validated row counts and reconciled source and target data.
* Built an analytics-ready Snowflake warehouse suitable for Power BI and advanced SQL analytics.

---

# Outcome

By the end of Day 13, the RetailIQ project contains a fully functional Snowflake data warehouse with a validated Star Schema. The warehouse is optimized for business intelligence reporting, analytical SQL, and downstream machine learning workloads.
