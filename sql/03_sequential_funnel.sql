/*
============================================================
E-COMMERCE FUNNEL ANALYSIS
File: 03_sequential_funnel.sql
============================================================

PURPOSE:
Calculate the e-commerce funnel while verifying that
events happened in chronological order.

BUSINESS QUESTIONS:
1. How many unique visitors viewed a product?
2. How many visitors viewed before adding to cart?
3. How many visitors added to cart before purchasing?
4. How many visitors completed the full funnel?
5. What are the sequential conversion rates?

FUNNEL:

    VIEW
      ↓
  ADD TO CART
      ↓
   PURCHASE

IMPORTANT:
This is a chronological funnel. Events must occur in the
correct order to be counted.

DATA LIMITATION:
The dataset may capture only part of a visitor's journey.
Therefore, absence of an event does not necessarily mean
that the visitor never performed that action.
*/


-- ============================================================
-- 1. FIND THE FIRST TIME EACH VISITOR PERFORMED EACH EVENT
-- ============================================================

WITH first_events AS (

    SELECT
        visitorid,

        -- First recorded product view
        MIN(
            CASE
                WHEN event = 'view'
                THEN event_datetime
            END
        ) AS first_view,

        -- First recorded add-to-cart event
        MIN(
            CASE
                WHEN event = 'addtocart'
                THEN event_datetime
            END
        ) AS first_cart,

        -- First recorded purchase
        MIN(
            CASE
                WHEN event = 'transaction'
                THEN event_datetime
            END
        ) AS first_purchase

    FROM events

    GROUP BY visitorid
),


-- ============================================================
-- 2. CHECK WHETHER EVENTS OCCURRED IN THE CORRECT ORDER
-- ============================================================

sequential_funnel AS (

    SELECT
        visitorid,
        first_view,
        first_cart,
        first_purchase,

        /*
        View → Cart

        The visitor must have both events and the view
        must happen before the cart.
        */
        CASE
            WHEN first_view IS NOT NULL
             AND first_cart IS NOT NULL
             AND first_view < first_cart
            THEN 1
            ELSE 0
        END AS view_to_cart,


        /*
        Cart → Purchase

        The visitor must have both events and the cart
        must happen before the purchase.
        */
        CASE
            WHEN first_cart IS NOT NULL
             AND first_purchase IS NOT NULL
             AND first_cart < first_purchase
            THEN 1
            ELSE 0
        END AS cart_to_purchase

    FROM first_events
),


-- ============================================================
-- 3. IDENTIFY USERS WHO COMPLETED THE FULL FUNNEL
-- ============================================================

final_funnel AS (

    SELECT
        visitorid,
        first_view,
        first_cart,
        first_purchase,
        view_to_cart,
        cart_to_purchase,

        /*
        Full funnel requires:

        View → Cart
        AND
        Cart → Purchase
        */
        CASE
            WHEN view_to_cart = 1
             AND cart_to_purchase = 1
            THEN 1
            ELSE 0
        END AS full_funnel

    FROM sequential_funnel
)


-- ============================================================
-- 4. DISPLAY THE RESULT
-- ============================================================

SELECT *
FROM final_funnel
LIMIT 20;

/*
============================================================
5. CALCULATE SEQUENTIAL FUNNEL METRICS
============================================================

Business Questions:
1. How many visitors viewed a product?
2. How many visitors viewed before adding to cart?
3. How many visitors added to cart before purchasing?
4. How many visitors completed the full funnel?
5. What are the sequential conversion rates?
*/

WITH first_events AS (

    SELECT
        visitorid,

        -- First recorded view
        MIN(
            CASE
                WHEN event = 'view'
                THEN event_datetime
            END
        ) AS first_view,

        -- First recorded cart addition
        MIN(
            CASE
                WHEN event = 'addtocart'
                THEN event_datetime
            END
        ) AS first_cart,

        -- First recorded purchase
        MIN(
            CASE
                WHEN event = 'transaction'
                THEN event_datetime
            END
        ) AS first_purchase

    FROM events

    GROUP BY visitorid
),

sequential_funnel AS (

    SELECT
        visitorid,
        first_view,
        first_cart,
        first_purchase,

        -- View happened before Cart
        CASE
            WHEN first_view IS NOT NULL
             AND first_cart IS NOT NULL
             AND first_view < first_cart
            THEN 1
            ELSE 0
        END AS view_to_cart,

        -- Cart happened before Purchase
        CASE
            WHEN first_cart IS NOT NULL
             AND first_purchase IS NOT NULL
             AND first_cart < first_purchase
            THEN 1
            ELSE 0
        END AS cart_to_purchase

    FROM first_events
),

final_funnel AS (

    SELECT
        visitorid,
        first_view,
        first_cart,
        first_purchase,
        view_to_cart,
        cart_to_purchase,

        -- Full funnel:
        -- View → Cart → Purchase
        CASE
            WHEN view_to_cart = 1
             AND cart_to_purchase = 1
            THEN 1
            ELSE 0
        END AS full_funnel

    FROM sequential_funnel
)

SELECT

    -- Total visitors who have a recorded view
    COUNT(
        CASE
            WHEN first_view IS NOT NULL
            THEN 1
        END
    ) AS view_users,

    -- Visitors whose view happened before cart
    SUM(view_to_cart) AS view_to_cart_users,

    -- Visitors whose cart happened before purchase
    SUM(cart_to_purchase) AS cart_to_purchase_users,

    -- Visitors completing View → Cart → Purchase
    SUM(full_funnel) AS full_funnel_users

FROM final_funnel;