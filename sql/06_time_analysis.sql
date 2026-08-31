/*
============================================================
E-COMMERCE TIME-BASED ANALYSIS
File: 06_time_analysis.sql
Dataset: RetailRocket E-commerce Dataset
============================================================

PURPOSE:
Analyze customer activity and conversion patterns based
on date, day of week, and hour of day.

BUSINESS QUESTIONS:

1. What is the date range of the dataset?
2. How many events occur on each day?
3. How many unique visitors are active each day?
4. Which days of the week have the most activity?
5. Which hours of the day have the most activity?
6. Which days have the highest conversion rates?
7. Which hours have the highest conversion rates?

CONVERSION METRICS:

View → Cart
Cart → Purchase
View → Purchase

IMPORTANT:
These are observational patterns. They show when users
converted more frequently, but they do not prove that the
time of day or day of week caused the higher conversion.
*/

-- ============================================================
-- 1. DATASET DATE RANGE
-- ============================================================

SELECT
    MIN(event_datetime) AS start_datetime,
    MAX(event_datetime) AS end_datetime
FROM events;

-- ============================================================
-- 2. DAILY EVENT VOLUME
-- ============================================================

SELECT
    event_datetime::date AS event_date,

    COUNT(*) FILTER (
        WHERE event = 'view'
    ) AS views,

    COUNT(*) FILTER (
        WHERE event = 'addtocart'
    ) AS add_to_cart,

    COUNT(*) FILTER (
        WHERE event = 'transaction'
    ) AS purchases

FROM events

GROUP BY
    event_datetime::date

ORDER BY
    event_date;

    -- ============================================================
-- 3. DAILY UNIQUE USERS
-- ============================================================

SELECT
    event_datetime::date AS event_date,

    COUNT(DISTINCT visitorid) FILTER (
        WHERE event = 'view'
    ) AS view_users,

    COUNT(DISTINCT visitorid) FILTER (
        WHERE event = 'addtocart'
    ) AS cart_users,

    COUNT(DISTINCT visitorid) FILTER (
        WHERE event = 'transaction'
    ) AS purchase_users

FROM events

GROUP BY
    event_datetime::date

ORDER BY
    event_date;

    -- ============================================================
-- 4. UNIQUE USERS BY DAY OF WEEK
-- ============================================================

SELECT
    EXTRACT(
        ISODOW FROM event_datetime
    ) AS day_number,

    TRIM(
        TO_CHAR(event_datetime, 'Day')
    ) AS day_of_week,

    COUNT(DISTINCT visitorid) FILTER (
        WHERE event = 'view'
    ) AS view_users,

    COUNT(DISTINCT visitorid) FILTER (
        WHERE event = 'addtocart'
    ) AS cart_users,

    COUNT(DISTINCT visitorid) FILTER (
        WHERE event = 'transaction'
    ) AS purchase_users

FROM events

GROUP BY
    EXTRACT(ISODOW FROM event_datetime),
    TRIM(TO_CHAR(event_datetime, 'Day'))

ORDER BY
    day_number;

    -- ============================================================
-- 5. UNIQUE USERS BY HOUR
-- ============================================================

SELECT
    EXTRACT(
        HOUR FROM event_datetime
    ) AS hour,

    COUNT(DISTINCT visitorid) FILTER (
        WHERE event = 'view'
    ) AS view_users,

    COUNT(DISTINCT visitorid) FILTER (
        WHERE event = 'addtocart'
    ) AS cart_users,

    COUNT(DISTINCT visitorid) FILTER (
        WHERE event = 'transaction'
    ) AS purchase_users

FROM events

GROUP BY
    EXTRACT(HOUR FROM event_datetime)

ORDER BY
    hour;

    -- ============================================================
-- 6. DAY-OF-WEEK CONVERSION
-- ============================================================

WITH weekday_users AS (

    SELECT
        EXTRACT(
            ISODOW FROM event_datetime
        ) AS day_number,

        TRIM(
            TO_CHAR(event_datetime, 'Day')
        ) AS day_of_week,

        COUNT(DISTINCT visitorid) FILTER (
            WHERE event = 'view'
        ) AS view_users,

        COUNT(DISTINCT visitorid) FILTER (
            WHERE event = 'addtocart'
        ) AS cart_users,

        COUNT(DISTINCT visitorid) FILTER (
            WHERE event = 'transaction'
        ) AS purchase_users

    FROM events

    GROUP BY
        EXTRACT(ISODOW FROM event_datetime),
        TRIM(TO_CHAR(event_datetime, 'Day'))
)

SELECT
    day_of_week,

    view_users,
    cart_users,
    purchase_users,

    ROUND(
        cart_users::numeric
        / NULLIF(view_users, 0)
        * 100,
        2
    ) AS view_to_cart_rate,

    ROUND(
        purchase_users::numeric
        / NULLIF(cart_users, 0)
        * 100,
        2
    ) AS cart_to_purchase_rate,

    ROUND(
        purchase_users::numeric
        / NULLIF(view_users, 0)
        * 100,
        2
    ) AS view_to_purchase_rate

FROM weekday_users

ORDER BY
    day_number;

    -- ============================================================
-- 7. HOURLY CONVERSION
-- ============================================================

WITH hourly_users AS (

    SELECT
        EXTRACT(
            HOUR FROM event_datetime
        ) AS hour,

        COUNT(DISTINCT visitorid) FILTER (
            WHERE event = 'view'
        ) AS view_users,

        COUNT(DISTINCT visitorid) FILTER (
            WHERE event = 'addtocart'
        ) AS cart_users,

        COUNT(DISTINCT visitorid) FILTER (
            WHERE event = 'transaction'
        ) AS purchase_users

    FROM events

    GROUP BY
        EXTRACT(HOUR FROM event_datetime)
)

SELECT
    hour,

    view_users,
    cart_users,
    purchase_users,

    ROUND(
        cart_users::numeric
        / NULLIF(view_users, 0)
        * 100,
        2
    ) AS view_to_cart_rate,

    ROUND(
        purchase_users::numeric
        / NULLIF(cart_users, 0)
        * 100,
        2
    ) AS cart_to_purchase_rate,

    ROUND(
        purchase_users::numeric
        / NULLIF(view_users, 0)
        * 100,
        2
    ) AS view_to_purchase_rate

FROM hourly_users

ORDER BY
    view_to_purchase_rate DESC;