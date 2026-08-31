/*
============================================================
E-COMMERCE CART ABANDONMENT ANALYSIS
File: 04_cart_abandonment.sql
Dataset: RetailRocket E-commerce Dataset
============================================================

PURPOSE:
Identify visitor-product pairs that added a product to the
cart and determine whether the product was subsequently
purchased or abandoned.

BUSINESS QUESTIONS:

1. How many visitor-product pairs added a product to cart?
2. How many cart pairs resulted in a purchase?
3. How many cart pairs were abandoned?
4. What is the cart abandonment rate?
5. What percentage of cart pairs converted to purchase?

ANALYSIS LEVEL:

Visitor + Product

Example:

Visitor 100 + Product 500
        ↓
     Add Cart
        ↓
   ┌────┴────┐
   ↓         ↓
Purchase   Abandoned

IMPORTANT:
A cart is considered "Purchased" only when a transaction
for the same visitor and product occurred AFTER the
add-to-cart event.

DATA LIMITATION:
The dataset may not capture every stage of a customer's
journey. Therefore, an "abandoned" cart means that no
subsequent purchase event was recorded in this dataset.
It does not necessarily prove that the customer never
purchased the product elsewhere or through an unrecorded
interaction.
*/
-- ============================================================
-- 1. FIND FIRST CART AND PURCHASE BY VISITOR + PRODUCT
-- ============================================================

WITH first_events AS (

    SELECT
        visitorid,
        itemid,

        -- First time this visitor added this product to cart
        MIN(
            CASE
                WHEN event = 'addtocart'
                THEN event_datetime
            END
        ) AS first_cart,

        -- First time this visitor purchased this product
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

SELECT *
FROM first_events
LIMIT 20;
/*
-- ============================================================
-- 2. IDENTIFY VALID CART → PURCHASE SEQUENCES
-- ============================================================

A purchase counts only when:

    first_cart < first_purchase
*/

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
),

cart_pairs AS (

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

    -- Keep only visitor-product pairs that actually
    -- added the product to the cart.
    WHERE first_cart IS NOT NULL
)

SELECT *
FROM cart_pairs
LIMIT 20;

-- ============================================================
-- 3. CART ABANDONMENT SUMMARY
-- ============================================================

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
),

cart_pairs AS (

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

    WHERE first_cart IS NOT NULL
)

SELECT

    COUNT(*) AS total_cart_pairs,

    COUNT(
        CASE
            WHEN status = 'Purchased'
            THEN 1
        END
    ) AS purchased_pairs,

    COUNT(
        CASE
            WHEN status = 'Abandoned'
            THEN 1
        END
    ) AS abandoned_pairs,

    ROUND(
        COUNT(
            CASE
                WHEN status = 'Abandoned'
                THEN 1
            END
        )::numeric
        / COUNT(*)
        * 100,
        2
    ) AS abandonment_rate,

    ROUND(
        COUNT(
            CASE
                WHEN status = 'Purchased'
                THEN 1
            END
        )::numeric
        / COUNT(*)
        * 100,
        2
    ) AS cart_to_purchase_rate

FROM cart_pairs;

