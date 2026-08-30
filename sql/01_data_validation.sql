 ---============================================================
-- 1. TOTAL ROW COUNT
-- Business Question:
-- How many event records are present in the dataset?
-- ============================================================

SELECT
    COUNT(*) AS total_rows
FROM events;

-- ============================================================
-- 2. EVENT DISTRIBUTION
-- Business Question:
-- What types of events are recorded and how frequently?
-- ============================================================
SELECT
    event,
    COUNT(*) AS event_count
FROM events
GROUP BY event
ORDER BY event_count DESC;

-- ============================================================
-- 3. UNIQUE VISITORS
-- Business Question:
-- How many distinct visitors interacted with the platform?
-- ============================================================
SELECT
    COUNT(DISTINCT visitorid) AS unique_visitors
FROM events;

-- ============================================================
-- 4. UNIQUE PRODUCTS
-- Business Question:
-- How many distinct products are present in the dataset?
-- ============================================================

SELECT
    COUNT(DISTINCT itemid) AS unique_products
FROM events;

-- ============================================================
-- 5. MISSING VALUES
-- Business Question:
-- Are important fields missing from the dataset?
-- ============================================================
SELECT
    COUNT(*) - COUNT(timestamp) AS missing_timestamp,
    COUNT(*) - COUNT(visitorid) AS missing_visitorid,
    COUNT(*) - COUNT(event) AS missing_event,
    COUNT(*) - COUNT(itemid) AS missing_itemid,
    COUNT(*) - COUNT(transactionid) AS missing_transactionid,
    COUNT(*) - COUNT(event_datetime) AS missing_event_datetime
FROM events;

-- ============================================================
-- 6. DATE RANGE
-- Business Question:
-- What period of time does the dataset cover?
-- ============================================================
SELECT
   MIN(event_datetime) AS start_date,
   MAX(event_datetime) AS end_date
FROM events;

-- ============================================================
-- 7. DUPLICATE RECORDS
-- Business Question:
-- Are duplicate event records present?
-- ============================================================
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT (
        timestamp,
        visitorid,
        event,
        itemid,
        transactionid
    )) AS unique_event_rows
FROM events;



SELECT
    COUNT(*) -
    COUNT(DISTINCT (
        timestamp,
        visitorid,
        event,
        itemid,
        transactionid
    )) AS duplicate_rows
FROM events;
