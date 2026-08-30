"""
E-commerce Funnel Drop-off Analysis
File: 04_sequential_funnel.py

Dataset:
RetailRocket E-commerce Dataset

Purpose:
Build a chronological, user-level e-commerce funnel by checking
whether visitors progressed through the stages in the expected order:

View → Add to Cart → Purchase

Business Questions:
1. How many visitors recorded a product view?
2. How many visitors subsequently added a product to the cart?
3. How many visitors subsequently recorded a purchase?
4. How many visitors completed the full View → Cart → Purchase journey?
5. What are the conversion rates between the sequential funnel stages?
6. How does the sequential funnel differ from the basic user-level
   funnel?

Method:
For each visitor, the first recorded timestamp for each event type
is identified. The funnel is considered sequential only when:

View < Add to Cart < Purchase

Important Limitation:
This is a visitor-level sequential funnel, not a visitor-product-level
funnel. Therefore, the view, cart, and purchase events do not necessarily
refer to the same product.
"""

import pandas as pd


# ============================================================
# 1. LOAD AND PREPARE DATA
# ============================================================

# Load the raw RetailRocket event dataset.
df = pd.read_csv(
    "../data/raw/events.csv"
)

# Convert the Unix timestamp from milliseconds into a
# readable datetime column.
df["datetime"] = pd.to_datetime(
    df["timestamp"],
    unit="ms"
)


# ============================================================
# 2. SORT EVENTS CHRONOLOGICALLY
# ============================================================

# Business Question:
# Can we determine the order in which each visitor performed
# different types of events?

# Sort events by visitor and timestamp so the user journey
# can be evaluated chronologically.
df = df.sort_values(
    ["visitorid", "datetime"]
)

print("Data sorted successfully.")

print("\n========== FIRST 20 EVENTS ==========")

print(
    df[
        [
            "visitorid",
            "datetime",
            "event",
            "itemid"
        ]
    ].head(20)
)


# ============================================================
# 3. FIND FIRST OCCURRENCE OF EACH EVENT
# ============================================================

# Business Question:
# For each visitor, when did their first view, first cart
# addition, and first purchase occur?

# The minimum timestamp gives the first recorded occurrence
# of each event for every visitor.
first_events = (
    df.groupby(
        ["visitorid", "event"]
    )["datetime"]
      .min()
      .unstack()
)

print("\n========== FIRST EVENT TIMESTAMPS ==========")

print(
    first_events.head()
)


# ============================================================
# 4. IDENTIFY FUNNEL STAGES
# ============================================================

# Check whether each visitor has a recorded event at each
# stage of the funnel.

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
# 5. CHECK CHRONOLOGICAL FUNNEL PROGRESSION
# ============================================================

# Business Question:
# Did the visitor's recorded events occur in the expected
# funnel order?

# A valid View → Cart progression requires both events to
# exist and the first view to occur before the first cart.
first_events["view_to_cart"] = (
    first_events["view"].notna()
    & first_events["addtocart"].notna()
    & (
        first_events["view"]
        < first_events["addtocart"]
    )
)


# A valid Cart → Purchase progression requires both events
# to exist and the first cart to occur before the first purchase.
first_events["cart_to_purchase"] = (
    first_events["addtocart"].notna()
    & first_events["transaction"].notna()
    & (
        first_events["addtocart"]
        < first_events["transaction"]
    )
)


# ============================================================
# 6. IDENTIFY COMPLETE SEQUENTIAL FUNNEL
# ============================================================

# Business Question:
# How many visitors completed the entire chronological
# View → Cart → Purchase journey?

first_events["full_funnel"] = (
    first_events["view_to_cart"]
    & first_events["cart_to_purchase"]
)


# ============================================================
# 7. SEQUENTIAL FUNNEL COUNTS
# ============================================================

print("\n========== SEQUENTIAL FUNNEL ==========")

view_users = (
    first_events["has_view"].sum()
)

view_to_cart_users = (
    first_events["view_to_cart"].sum()
)

cart_to_purchase_users = (
    first_events["cart_to_purchase"].sum()
)

full_funnel_users = (
    first_events["full_funnel"].sum()
)


print(
    f"Users who viewed: "
    f"{view_users:,}"
)

print(
    f"Users who viewed → cart: "
    f"{view_to_cart_users:,}"
)

print(
    f"Users who carted → purchased: "
    f"{cart_to_purchase_users:,}"
)

print(
    f"Users completing full funnel: "
    f"{full_funnel_users:,}"
)


# ============================================================
# 8. SEQUENTIAL CONVERSION RATES
# ============================================================

# Business Question:
# What percentage of visitors successfully progressed through
# each chronological funnel stage?

view_to_cart_rate = (
    view_to_cart_users
    / view_users
    * 100
)

cart_to_purchase_rate = (
    cart_to_purchase_users
    / view_to_cart_users
    * 100
)

overall_conversion = (
    full_funnel_users
    / view_users
    * 100
)


print("\n========== SEQUENTIAL CONVERSION ==========")

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
    f"{overall_conversion:.2f}%"
)