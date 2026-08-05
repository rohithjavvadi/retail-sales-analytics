# Day 15 – Business Analytics with Snowflake SQL

## Objective

The goal of Day 15 was to transform the RetailIQ data warehouse into a business analytics layer by writing SQL queries that answer real business questions. These queries will be reused in the upcoming Streamlit dashboard.

---

## What We Built

### Executive KPIs

* Total Revenue
* Total Orders
* Total Customers
* Average Order Value (AOV)
* Average Items per Order
* Average Revenue per Customer

### Sales Analysis

* Revenue by Month
* Revenue by Customer State
* Revenue by Product Category
* Top 10 Products
* Top 10 Sellers

### Customer Analysis

* Top Customers by Revenue
* Customer Order Frequency
* Average Customer Spend
* Customer Ranking using `RANK()`
* Customer Lifetime Value (CLV)

### Product Analysis

* Top Performing Products
* Revenue by Product Category
* Category Ranking using `DENSE_RANK()`

### Time Analysis

* Monthly Revenue
* Previous Month Revenue using `LAG()`
* Running Total Revenue using Window Functions
* Quarterly Revenue
* Weekend vs Weekday Sales

---

## SQL Concepts Practiced

* INNER JOIN
* Aggregate Functions (`SUM`, `COUNT`, `AVG`)
* `GROUP BY`
* `ORDER BY`
* Common Table Expressions (CTEs)
* Window Functions

  * `RANK()`
  * `DENSE_RANK()`
  * `LAG()`
  * `SUM() OVER()`
* Business KPI calculations

---

## Challenges Faced

### 1. Column Name Mismatches

Some initial queries used generic names such as `TOTAL_SALE_AMOUNT` and `ORDER_DATE_KEY`, which did not exist in the Snowflake warehouse.

**Resolution**

Updated the queries to use the actual warehouse schema:

* `PAYMENT_VALUE` for revenue
* `DATE_KEY` for the date dimension foreign key
* `PRODUCT_CATEGORY_NAME_ENGLISH` for product categories

---

### 2. Schema Validation

Before finalizing the analytics queries, each dimension table was inspected using `DESC TABLE` to verify the available columns.

This ensured that every query matched the warehouse structure exactly.

---

## Business Value

The analytics layer enables stakeholders to:

* Monitor overall business performance.
* Identify high-performing customers and sellers.
* Analyze product category performance.
* Track monthly and quarterly revenue trends.
* Measure customer lifetime value.
* Support interactive filtering and reporting.

---

## Deliverables

```
sql/
└── 05_business_analytics.sql

docs/
└── DAY15_BUSINESS_ANALYTICS.md
```

---

## Next Step

Day 16 focuses on building the **Streamlit analytics dashboard**. The dashboard will connect directly to Snowflake, execute these SQL queries, and present the results through KPI cards, interactive charts, filters, and tables. This becomes the presentation layer of the RetailIQ Analytics Platform.
