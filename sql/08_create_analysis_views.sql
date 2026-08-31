/*
============================================================
POWER BI ANALYTICAL VIEWS
File: 08_create_analysis_views.sql
Dataset: RetailRocket E-commerce Dataset
============================================================

PURPOSE:

Create reusable PostgreSQL views containing the main
analytical outputs of the project.

These views will act as the reporting layer between
PostgreSQL and Power BI.

VIEWS CREATED:

1. vw_funnel_summary
2. vw_cart_abandonment
3. vw_product_opportunities
4. vw_time_analysis
5. vw_user_engagement

BUSINESS PURPOSE:

Instead of performing complex calculations repeatedly
inside Power BI, the major analytical transformations
are performed in PostgreSQL.

Power BI can then connect directly to these views.

DATA FLOW:

Raw Events
    ↓
PostgreSQL
    ↓
Analytical Views
    ↓
Power BI
    ↓
Dashboard
*/


-- ============================================================
-- 1. FUNNEL SUMMARY VIEW
-- ============================================================

CREATE OR REPLACE VIEW vw_funnel_summary AS

WITH first_events AS (

    SELECT
        visitorid,

        MIN(
            CASE
                WHEN event = 'view'
                THEN event_datetime
            END
        ) AS first_view,

        MIN(
            CASE
                WHEN event = 'addtocart'
                THEN event_datetime
            END
        ) AS first_cart,

        MIN(
            CASE
                WHEN event = 'transaction'
                THEN event_datetime
            END
        ) AS first_purchase

    FROM events

    GROUP BY visitorid
),

funnel AS (

    SELECT
        visitorid,
        first_view,
        first_cart,
        first_purchase,

        CASE
            WHEN first_view IS NOT NULL
             AND first_cart IS NOT NULL
             AND first_view < first_cart
            THEN 1
            ELSE 0
        END AS view_to_cart,

        CASE
            WHEN first_cart IS NOT NULL
             AND first_purchase IS NOT NULL
             AND first_cart < first_purchase
            THEN 1
            ELSE 0
        END AS cart_to_purchase

    FROM first_events
)

SELECT

    COUNT(*) FILTER (
        WHERE first_view IS NOT NULL
    ) AS view_users,

    SUM(view_to_cart) AS view_to_cart_users,

    SUM(cart_to_purchase) AS cart_to_purchase_users,

    SUM(
        CASE
            WHEN view_to_cart = 1
             AND cart_to_purchase = 1
            THEN 1
            ELSE 0
        END
    ) AS full_funnel_users

FROM funnel;


-- ============================================================
-- 2. CART ABANDONMENT VIEW
-- ============================================================

CREATE OR REPLACE VIEW vw_cart_abandonment AS

WITH first_events AS (

    SELECT
        visitorid,
        itemid,

        MIN(
            CASE
                WHEN event = 'addtocart'
                THEN event_datetime
            END
        ) AS first_cart,

        MIN(
            CASE
                WHEN event = 'transaction'
                THEN event_datetime
            END
        ) AS first_purchase

    FROM events

    GROUP BY
        visitorid,
        itemid
)

SELECT

    visitorid,
    itemid,
    first_cart,
    first_purchase,

    CASE

        WHEN first_purchase IS NOT NULL
         AND first_cart < first_purchase
        THEN 'Purchased'

        ELSE 'Abandoned'

    END AS status

FROM first_events

WHERE first_cart IS NOT NULL;