/*
============================================================
E-COMMERCE PRODUCT OPPORTUNITY ANALYSIS
File: 05_product_opportunities.sql
Dataset: RetailRocket E-commerce Dataset
============================================================

PURPOSE:
Identify products that have significant cart activity but
also experience high cart abandonment.

BUSINESS QUESTIONS:

1. Which products are added to cart most frequently?
2. Which products have the highest number of abandoned carts?
3. Which products have high cart abandonment rates?
4. Which products represent the biggest opportunities
   for further investigation?

ANALYSIS LEVEL:

Visitor + Product → Product

The analysis first determines whether each visitor-product
cart resulted in a subsequent purchase.

A product is then evaluated using:

- Cart pairs
- Purchased pairs
- Abandoned pairs
- Abandonment rate
- Purchase rate

IMPORTANT:
Products with very few cart events can produce misleadingly
high abandonment rates.

Therefore, a minimum cart-volume threshold is applied.

DATA LIMITATION:
An "abandoned" cart means that no subsequent purchase event
was recorded for that visitor-product pair in this dataset.
It does not prove that the customer never purchased the
product through another unrecorded interaction.
*/

-- ============================================================
-- 1. FIND FIRST CART AND PURCHASE BY VISITOR + PRODUCT
-- ============================================================

WITH first_events AS (

    SELECT
        visitorid,
        itemid,

        -- First recorded cart event
        MIN(
            CASE
                WHEN event = 'addtocart'
                THEN event_datetime
            END
        ) AS first_cart,

        -- First recorded purchase event
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

        /*
        A cart is considered purchased only when the
        purchase occurred after the cart event.
        */
        CASE
            WHEN first_purchase IS NOT NULL
             AND first_cart < first_purchase
            THEN 'Purchased'
            ELSE 'Abandoned'
        END AS status

    FROM first_events

    -- Only keep visitor-product pairs that added
    -- the product to the cart.
    WHERE first_cart IS NOT NULL
)

SELECT *
FROM cart_pairs
LIMIT 20;

-- ============================================================
-- 2. PRODUCT-LEVEL CART SUMMARY
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

        CASE
            WHEN first_purchase IS NOT NULL
             AND first_cart < first_purchase
            THEN 'Purchased'
            ELSE 'Abandoned'
        END AS status

    FROM first_events

    WHERE first_cart IS NOT NULL
),

product_summary AS (

    SELECT
        itemid,

        -- Total visitor-product cart pairs
        COUNT(*) AS cart_pairs,

        -- Successful purchases
        COUNT(
            CASE
                WHEN status = 'Purchased'
                THEN 1
            END
        ) AS purchased_pairs,

        -- Abandoned carts
        COUNT(
            CASE
                WHEN status = 'Abandoned'
                THEN 1
            END
        ) AS abandoned_pairs

    FROM cart_pairs

    GROUP BY itemid
)

SELECT *
FROM product_summary
ORDER BY cart_pairs DESC
LIMIT 20;

-- ============================================================
-- 3. CALCULATE PRODUCT CONVERSION RATES
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

        CASE
            WHEN first_purchase IS NOT NULL
             AND first_cart < first_purchase
            THEN 'Purchased'
            ELSE 'Abandoned'
        END AS status

    FROM first_events

    WHERE first_cart IS NOT NULL
),

product_summary AS (

    SELECT
        itemid,

        COUNT(*) AS cart_pairs,

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
        ) AS abandoned_pairs

    FROM cart_pairs

    GROUP BY itemid
)

SELECT
    itemid,
    cart_pairs,
    purchased_pairs,
    abandoned_pairs,

    ROUND(
        abandoned_pairs::numeric
        / NULLIF(cart_pairs, 0)
        * 100,
        2
    ) AS abandonment_rate,

    ROUND(
        purchased_pairs::numeric
        / NULLIF(cart_pairs, 0)
        * 100,
        2
    ) AS purchase_rate

FROM product_summary

ORDER BY cart_pairs DESC

LIMIT 20;

-- ============================================================
-- 4. FINAL PRODUCT OPPORTUNITIES
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

        CASE
            WHEN first_purchase IS NOT NULL
             AND first_cart < first_purchase
            THEN 'Purchased'
            ELSE 'Abandoned'
        END AS status

    FROM first_events

    WHERE first_cart IS NOT NULL
),

product_summary AS (

    SELECT
        itemid,

        COUNT(*) AS cart_pairs,

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
        ) AS abandoned_pairs

    FROM cart_pairs

    GROUP BY itemid
),

product_rates AS (

    SELECT
        itemid,
        cart_pairs,
        purchased_pairs,
        abandoned_pairs,

        ROUND(
            abandoned_pairs::numeric
            / NULLIF(cart_pairs, 0)
            * 100,
            2
        ) AS abandonment_rate,

        ROUND(
            purchased_pairs::numeric
            / NULLIF(cart_pairs, 0)
            * 100,
            2
        ) AS purchase_rate

    FROM product_summary
)

SELECT
    itemid,
    cart_pairs,
    purchased_pairs,
    abandoned_pairs,
    abandonment_rate,
    purchase_rate

FROM product_rates

-- Ignore products with very small cart samples
WHERE cart_pairs >= 100

-- Prioritize products with the largest number
-- of abandoned visitor-product pairs.
ORDER BY
    abandoned_pairs DESC,
    abandonment_rate DESC

LIMIT 15;