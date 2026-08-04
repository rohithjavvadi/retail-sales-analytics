-- =====================================================
-- RetailIQ Analytics Platform
-- Day 14 - Top Product Recommendations
-- =====================================================
-- Purpose:
-- Create business-ready recommendation views using the
-- recommendation engine built from product affinity analysis.
--
-- Author: Rohith Javvadi
-- =====================================================

USE DATABASE RETAILIQ_DB;
USE SCHEMA ANALYTICS;

---------------------------------------------------------
-- Top 5 Recommendations Per Product
---------------------------------------------------------

CREATE OR REPLACE VIEW VW_TOP_PRODUCT_RECOMMENDATIONS AS

SELECT
    PRODUCT_KEY,
    RECOMMENDED_PRODUCT_KEY,
    RECOMMENDATION_SCORE,
    RECOMMENDATION_RANK

FROM PRODUCT_RECOMMENDATIONS_RANKED

WHERE RECOMMENDATION_RANK <= 5;

---------------------------------------------------------
-- Business-Friendly Recommendation View
---------------------------------------------------------

CREATE OR REPLACE VIEW VW_PRODUCT_RECOMMENDATIONS AS

SELECT

    p1.PRODUCT_KEY,
    p1.PRODUCT_CATEGORY_NAME_ENGLISH AS PRODUCT_CATEGORY,

    p2.PRODUCT_KEY AS RECOMMENDED_PRODUCT_KEY,
    p2.PRODUCT_CATEGORY_NAME_ENGLISH AS RECOMMENDED_CATEGORY,

    r.RECOMMENDATION_SCORE,
    r.RECOMMENDATION_RANK

FROM VW_TOP_PRODUCT_RECOMMENDATIONS r

JOIN DIM_PRODUCTS p1
ON r.PRODUCT_KEY = p1.PRODUCT_KEY

JOIN DIM_PRODUCTS p2
ON r.RECOMMENDED_PRODUCT_KEY = p2.PRODUCT_KEY

ORDER BY
    PRODUCT_CATEGORY,
    RECOMMENDATION_RANK;

---------------------------------------------------------
-- Validation
---------------------------------------------------------

SELECT COUNT(*) AS TOP_RECOMMENDATIONS
FROM VW_TOP_PRODUCT_RECOMMENDATIONS;

SELECT *
FROM VW_PRODUCT_RECOMMENDATIONS
LIMIT 20;