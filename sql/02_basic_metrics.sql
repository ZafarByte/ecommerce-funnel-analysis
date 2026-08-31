/*
E-commerce Funnel Drop-off Analysis
File: 02_basic_metrics.sql

Purpose:
Calculate the core e-commerce metrics used throughout
the analysis.

Business Questions:
1. How many total events were recorded?
2. How many unique visitors interacted with the platform?
3. How many users reached each funnel stage?
4. What is the basic View → Cart → Purchase conversion?
*/


-- ============================================================
-- 1. TOTAL EVENTS
-- Business Question:
-- How many total user events were recorded?
-- ============================================================

SELECT
    COUNT(*) AS total_events
FROM events;


-- ============================================================
-- 2. UNIQUE VISITORS
-- Business Question:
-- How many distinct visitors interacted with the platform?
-- ============================================================

SELECT
    COUNT(DISTINCT visitorid) AS unique_visitors
FROM events;

-- ============================================================
-- 3. UNIQUE USERS BY FUNNEL STAGE
-- Business Question:
-- How many unique visitors reached each funnel stage?
-- ============================================================

SELECT
    event,
    COUNT(DISTINCT visitorid) AS unique_users
FROM events
GROUP BY event
ORDER BY unique_users DESC;

-- ============================================================
-- 4. BASIC FUNNEL CONVERSION
-- Business Question:
-- What percentage of users moved between funnel stages?
-- ============================================================
WITH funnel AS (

    SELECT
        COUNT(DISTINCT CASE
            WHEN event = 'view'
            THEN visitorid
        END) AS view_users,

        COUNT(DISTINCT CASE
            WHEN event = 'addtocart'
            THEN visitorid
        END) AS cart_users,

        COUNT(DISTINCT CASE
            WHEN event = 'transaction'
            THEN visitorid
        END) AS purchase_users

    FROM events
)

SELECT
    view_users,
    cart_users,
    purchase_users,

    ROUND(
        cart_users * 100.0 / view_users,
        2
    ) AS view_to_cart_rate,

    ROUND(
        purchase_users * 100.0 / cart_users,
        2
    ) AS cart_to_purchase_rate,

    ROUND(
        purchase_users * 100.0 / view_users,
        2
    ) AS view_to_purchase_rate

FROM funnel;