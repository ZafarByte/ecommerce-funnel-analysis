"""
E-commerce Funnel Drop-off Analysis
File: 07_product_opportunities.py

Dataset:
RetailRocket E-commerce Dataset

Purpose:
Identify products with high cart volume and high observed
cart abandonment so that potential product-level opportunities
can be prioritized for further investigation.

Business Questions:
1. Which products receive the most cart additions?
2. Which products have the highest number of abandoned carts?
3. Which products have the highest cart abandonment rates?
4. Which products combine meaningful cart volume with high
   abandonment and may represent important business opportunities?

Method:
Cart behavior is analyzed at the visitor-product level.
Each visitor-product pair is classified as:

- Purchased: A recorded transaction occurred after the
  add-to-cart event.
- Abandoned: An add-to-cart event exists but no subsequent
  transaction was recorded.

A minimum threshold of 100 cart pairs is used when identifying
final product opportunities. This prevents products with very
small sample sizes from appearing as misleading high-abandonment
opportunities.

Important Data Limitation:
"Abandoned" means no subsequent transaction was recorded for the
visitor-product pair in the available dataset. It does not prove
that the user never purchased later or through another unobserved
journey.

Product IDs are used because the RetailRocket dataset does not
provide descriptive product names or categories in the events
table.
"""

import pandas as pd


# ============================================================
# 1. LOAD AND PREPARE DATA
# ============================================================

# Load the raw RetailRocket event dataset.
df = pd.read_csv(
    "../data/raw/events.csv"
)

# Convert Unix timestamp from milliseconds into a readable
# datetime column.
df["datetime"] = pd.to_datetime(
    df["timestamp"],
    unit="ms"
)

# Sort events chronologically for each visitor-product pair.
# This allows us to determine whether a purchase occurred
# after the cart addition.
df = df.sort_values(
    [
        "visitorid",
        "itemid",
        "datetime"
    ]
)

print("Data loaded successfully.")


# ============================================================
# 2. FIRST EVENT BY VISITOR + PRODUCT
# ============================================================

# Business Question:
# For each visitor-product pair, when did the first recorded
# view, add-to-cart, and transaction occur?

first_events = (
    df.groupby(
        [
            "visitorid",
            "itemid",
            "event"
        ]
    )["datetime"]
    .min()
    .unstack()
)


# ============================================================
# 3. IDENTIFY CART → PURCHASE PROGRESSION
# ============================================================

# Identify visitor-product pairs with a recorded cart event.
first_events["has_cart"] = (
    first_events["addtocart"].notna()
)


# Business Question:
# Did a purchase occur after the visitor added the same
# product to the cart?

first_events["cart_to_purchase"] = (
    first_events["addtocart"].notna()
    &
    first_events["transaction"].notna()
    &
    (
        first_events["addtocart"]
        < first_events["transaction"]
    )
)


# ============================================================
# 4. KEEP ONLY CART EVENTS
# ============================================================

# We only need visitor-product pairs that reached the
# add-to-cart stage for product-level cart analysis.
cart_pairs = first_events[
    first_events["has_cart"]
].copy()


# ============================================================
# 5. CLASSIFY CART OUTCOME
# ============================================================

# Business Question:
# What happened after each visitor-product pair added the
# product to the cart?

# Start by classifying all cart pairs as abandoned.
cart_pairs["status"] = "Abandoned"


# Change the status to Purchased when a transaction occurred
# after the cart event.
cart_pairs.loc[
    cart_pairs["cart_to_purchase"],
    "status"
] = "Purchased"


print("\n========== CART PAIRS ==========")

print(
    cart_pairs["status"].value_counts()
)


# ============================================================
# 6. CREATE PRODUCT-LEVEL SUMMARY
# ============================================================

# Business Question:
# How many cart additions, purchases, and abandoned carts
# are associated with each product?

product_summary = (
    cart_pairs
    .reset_index()
    .groupby("itemid")
    .agg(
        cart_pairs=(
            "visitorid",
            "count"
        ),

        purchased_pairs=(
            "status",
            lambda x: (
                x == "Purchased"
            ).sum()
        ),

        abandoned_pairs=(
            "status",
            lambda x: (
                x == "Abandoned"
            ).sum()
        )
    )
    .reset_index()
)


# ============================================================
# 7. CALCULATE PRODUCT-LEVEL RATES
# ============================================================

# Business Question:
# What percentage of each product's cart additions were
# followed by a purchase versus no recorded purchase?

product_summary["abandonment_rate"] = (
    product_summary["abandoned_pairs"]
    / product_summary["cart_pairs"]
    * 100
)

product_summary["purchase_rate"] = (
    product_summary["purchased_pairs"]
    / product_summary["cart_pairs"]
    * 100
)


# ============================================================
# 8. RANK PRODUCTS BY CART VOLUME
# ============================================================

# Business Question:
# Which products receive the highest number of cart additions?

# Sort products by cart volume so that products with the
# greatest observed cart activity appear first.
product_summary = (
    product_summary
    .sort_values(
        "cart_pairs",
        ascending=False
    )
)


print(
    "\n========== TOP PRODUCTS BY CART VOLUME =========="
)

print(
    product_summary
    .head(20)
    .to_string(index=False)
)


# ============================================================
# 9. IDENTIFY FINAL PRODUCT OPPORTUNITIES
# ============================================================

# Business Question:
# Which products combine meaningful cart volume with a high
# number of abandoned carts?
#
# A minimum of 100 cart pairs is required to reduce the impact
# of extremely small samples on the opportunity ranking.

final_opportunities = (
    product_summary[
        product_summary["cart_pairs"] >= 100
    ]
    .sort_values(
        [
            "abandoned_pairs",
            "abandonment_rate"
        ],
        ascending=[
            False,
            False
        ]
    )
)


print(
    "\n========== FINAL PRODUCT OPPORTUNITIES =========="
)

print(
    final_opportunities[
        [
            "itemid",
            "cart_pairs",
            "purchased_pairs",
            "abandoned_pairs",
            "abandonment_rate",
            "purchase_rate"
        ]
    ]
    .head(15)
    .to_string(index=False)
)