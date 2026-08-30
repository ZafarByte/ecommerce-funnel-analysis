"""
E-commerce Funnel Drop-off Analysis
File: 05_product_funnel.py

Dataset:
RetailRocket E-commerce Dataset

Purpose:
Build a chronological funnel at the visitor-product level.

Unlike the visitor-level funnel, this analysis checks whether
the same visitor interacted with the same product through the
recorded sequence:

View → Add to Cart → Purchase

Business Questions:
1. How many unique visitor-product combinations recorded a view?
2. How many visitor-product combinations progressed from view
   to add-to-cart?
3. How many visitor-product combinations progressed from
   add-to-cart to purchase?
4. How many visitor-product combinations completed the full
   View → Cart → Purchase journey?
5. What is the product-level funnel conversion rate?
6. Does adding the product dimension change our understanding
   of funnel performance?

Important Limitation:
The RetailRocket dataset contains an event log and may not capture
every step of a user's real-world journey. Therefore, a missing
event should be interpreted as "not recorded in this dataset",
not necessarily "the user never performed that action."

Additional Note:
This analysis evaluates the first recorded occurrence of each
event for a visitor-product pair.
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


# ============================================================
# 2. SORT EVENTS BY VISITOR, PRODUCT, AND TIME
# ============================================================

# Business Question:
# In what chronological order did each visitor interact
# with each product?

# Sorting by visitor, product, and time allows us to evaluate
# the sequence of events for each visitor-product combination.
df = df.sort_values(
    [
        "visitorid",
        "itemid",
        "datetime"
    ]
)

print("Data sorted successfully.")

print("\n========== SAMPLE ==========")

print(
    df[
        [
            "visitorid",
            "itemid",
            "datetime",
            "event"
        ]
    ].head(20)
)


# ============================================================
# 3. FIND FIRST EVENT FOR EACH VISITOR-PRODUCT PAIR
# ============================================================

# Business Question:
# When did each visitor first view, add to cart, or purchase
# a particular product?

# Group by visitor + product + event and retain the first
# recorded timestamp for each event type.
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

print(
    "\n========== FIRST EVENTS BY VISITOR + PRODUCT =========="
)

print(
    first_events.head(10)
)


# ============================================================
# 4. CHECK WHETHER EACH EVENT EXISTS
# ============================================================

# Determine whether each visitor-product pair has a recorded
# event at each stage of the funnel.

first_events["has_view"] = (
    first_events["view"].notna()
)

first_events["has_cart"] = (
    first_events["addtocart"].notna()
)

first_events["has_purchase"] = (
    first_events["transaction"].notna()
)


# ============================================================
# 5. CHECK VIEW → ADD TO CART SEQUENCE
# ============================================================

# Business Question:
# Did the visitor add the same product to the cart after
# first viewing that product?

first_events["view_to_cart"] = (
    first_events["view"].notna()
    &
    first_events["addtocart"].notna()
    &
    (
        first_events["view"]
        < first_events["addtocart"]
    )
)


# ============================================================
# 6. CHECK ADD TO CART → PURCHASE SEQUENCE
# ============================================================

# Business Question:
# Did the visitor purchase the same product after adding
# it to the cart?

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
# 7. IDENTIFY COMPLETE PRODUCT FUNNEL
# ============================================================

# Business Question:
# How many visitor-product combinations completed the full
# chronological View → Cart → Purchase journey?

first_events["full_funnel"] = (
    first_events["view_to_cart"]
    &
    first_events["cart_to_purchase"]
)


# ============================================================
# 8. PRODUCT-LEVEL FUNNEL COUNTS
# ============================================================

print("\n========== PRODUCT FUNNEL ==========")

view_product_pairs = (
    first_events["has_view"].sum()
)

view_cart_pairs = (
    first_events["view_to_cart"].sum()
)

cart_purchase_pairs = (
    first_events["cart_to_purchase"].sum()
)

full_funnel_pairs = (
    first_events["full_funnel"].sum()
)


print(
    f"Visitor-product views: "
    f"{view_product_pairs:,}"
)

print(
    f"Visitor-product view → cart: "
    f"{view_cart_pairs:,}"
)

print(
    f"Visitor-product cart → purchase: "
    f"{cart_purchase_pairs:,}"
)

print(
    f"Visitor-product full funnel: "
    f"{full_funnel_pairs:,}"
)


# ============================================================
# 9. PRODUCT-LEVEL FUNNEL CONVERSION
# ============================================================

# Business Question:
# What percentage of viewed visitor-product combinations
# progress through the product-level funnel?

# View → Cart conversion measures the percentage of viewed
# visitor-product pairs that subsequently reached cart.
view_to_cart_rate = (
    view_cart_pairs
    / view_product_pairs
    * 100
)

# Cart → Purchase conversion within the sequential funnel
# measures the percentage of view-to-cart pairs that also
# completed the recorded purchase stage.
cart_to_purchase_rate = (
    full_funnel_pairs
    / view_cart_pairs
    * 100
)

# Overall View → Purchase conversion measures the percentage
# of viewed visitor-product pairs that completed the full
# recorded funnel.
view_to_purchase_rate = (
    full_funnel_pairs
    / view_product_pairs
    * 100
)


print(
    "\n========== PRODUCT FUNNEL CONVERSION =========="
)

print(
    f"View → Cart: "
    f"{view_to_cart_rate:.2f}%"
)

print(
    f"Cart → Purchase: "
    f"{cart_to_purchase_rate:.2f}%"
)

print(
    f"View → Purchase: "
    f"{view_to_purchase_rate:.2f}%"
)