# Day 14 – Product Recommendation Engine

## Objective

The objective of Day 14 was to build a Product Recommendation Engine on top of the Snowflake data warehouse created in previous days. Instead of only storing transactional data, the warehouse was extended to generate product recommendations that can be consumed by business intelligence dashboards and future AI applications.

---

# What We Built

During this phase, the following objects were created:

* PRODUCT_AFFINITY table
* PRODUCT_RECOMMENDATIONS table
* PRODUCT_RECOMMENDATIONS_RANKED table
* VW_TOP_PRODUCT_RECOMMENDATIONS view
* VW_PRODUCT_RECOMMENDATIONS view

These objects together form a simple recommendation engine based on products frequently purchased together.

---

# Business Problem

Retail businesses often want to recommend products that customers are likely to purchase together.

Examples include:

* Amazon – "Frequently Bought Together"
* Walmart – "Customers Also Bought"
* Target – Product recommendations

The objective was to identify products appearing in the same customer orders and generate recommendations based on purchase frequency.

---

# Implementation Approach

## Step 1 – Product Affinity Analysis

The FACT_SALES table was joined with itself using a self join.

The join condition matched records belonging to the same ORDER_ID while ensuring that PRODUCT_KEY_1 was always less than PRODUCT_KEY_2.

This approach removed:

* duplicate product pairs
* reverse combinations
* self-pairs

The output was stored in the PRODUCT_AFFINITY table.

---

## Step 2 – Recommendation Engine

The PRODUCT_AFFINITY table only stored one direction of each product pair.

To support recommendations in both directions, two SELECT statements were combined using UNION ALL.

Example:

Laptop → Mouse

was expanded into

Laptop → Mouse

and

Mouse → Laptop

The result was stored in PRODUCT_RECOMMENDATIONS.

---

## Step 3 – Ranking Recommendations

ROW_NUMBER() was used to rank recommendations for every product based on recommendation score.

The ranking logic allows business applications to display only the highest quality recommendations instead of every available product pair.

---

## Step 4 – Business-Friendly View

The recommendation tables initially contained only surrogate product keys.

To improve readability, PRODUCT_KEY values were joined with DIM_PRODUCTS to retrieve PRODUCT_CATEGORY_NAME_ENGLISH.

This produced a view suitable for dashboards and reporting.

---

# Problems Encountered

## Problem 1

Business-friendly view failed because PRODUCT_NAME did not exist.

### Cause

The SQL initially assumed that DIM_PRODUCTS contained a PRODUCT_NAME column.

The Olist dataset does not include individual product names.

### Solution

The table schema was inspected using:

DESC TABLE DIM_PRODUCTS;

It was found that the correct descriptive column was:

PRODUCT_CATEGORY_NAME_ENGLISH

The business view was updated to use this column instead.

---

## Problem 2

Potential duplicate recommendations

### Cause

A self join naturally generates:

A → B

and

B → A

It can also generate:

A → A

### Solution

The following condition was applied during the self join:

PRODUCT_KEY_1 < PRODUCT_KEY_2

This eliminated self-pairs and duplicate reverse pairs.

---

## Problem 3

Recommendation ordering

### Cause

Business users only need the most relevant recommendations.

### Solution

ROW_NUMBER() was used to rank recommendations based on RECOMMENDATION_SCORE, and only the Top 5 recommendations were exposed through the reporting view.

---

# Validation Performed

The following validation checks were executed successfully.

### Product Affinity

* Product Affinity rows created: **4047**
* Self-pair validation returned **0 rows**

### Recommendation Engine

* Recommendation rows created: **8094**
* Duplicate recommendation validation returned **0 rows**

### Business Views

* Top recommendation view created successfully
* Business recommendation view generated successfully using PRODUCT_CATEGORY_NAME_ENGLISH

---

# Key SQL Concepts Practiced

* Self Join
* Aggregate Functions
* COUNT(DISTINCT)
* UNION ALL
* Window Functions
* ROW_NUMBER()
* Views
* Dimensional Modeling
* Recommendation Logic
* Data Validation

---

# Why This Approach Was Used

This implementation follows a common retail analytics pattern where historical purchase data is used to identify relationships between products.

Although simple, this co-occurrence approach is widely used as a baseline recommendation technique because it is:

* Easy to understand
* Fast to execute
* Scalable in SQL
* Suitable for dashboards
* A strong foundation for future machine learning recommendation systems

---

# Outcome

At the end of Day 14, the RetailIQ Analytics Platform was enhanced with a functional SQL-based recommendation engine capable of identifying products purchased together, ranking recommendations, and exposing business-friendly recommendation views for analytics and reporting.
