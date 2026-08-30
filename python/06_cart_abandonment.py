"""
E-commerce Funnel Drop-off Analysis
File: 06_cart_abandonment.py

Dataset:
RetailRocket E-commerce Dataset

Purpose:
Identify visitor-product cart additions that were followed by
a recorded purchase versus those with no subsequent recorded
purchase.

Business Questions:
1. How many visitor-product pairs added a product to the cart?
2. How many cart additions were followed by a recorded purchase?
3. How many cart additions had no subsequent recorded purchase?
4. What is the observed cart abandonment rate?
5. What percentage of observed cart additions converted to purchase?

Method:
For each visitor-product pair, the first recorded add-to-cart
and transaction timestamps are compared.

A cart is classified as:
- Purchased: A transaction occurred after the recorded cart event.
- Abandoned: A cart event exists but no subsequent transaction
  is recorded.

Important Data Limitation:
"Abandoned" means that no subsequent purchase event was recorded
for that visitor-product pair in the available dataset. It does
not prove that the user never purchased later or through another
unobserved journey.
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

print("Data loaded and sorted successfully.")


# ============================================================
# 2. FIRST EVENT TIME BY VISITOR + PRODUCT
# ============================================================

# Business Question:
# For each visitor-product pair, when was the first recorded
# add-to-cart event and first recorded transaction?

# Find the first recorded timestamp for every event type
# within each visitor-product combination.
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

print("\n========== FIRST EVENTS ==========")

print(
    first_events.head(10)
)


# ============================================================
# 3. IDENTIFY CART AND PURCHASE EVENTS
# ============================================================

# Determine whether a visitor-product pair has a recorded
# cart event and transaction event.
first_events["has_cart"] = (
    first_events["addtocart"].notna()
)

first_events["has_purchase"] = (
    first_events["transaction"].notna()
)


# Business Question:
# Did the purchase happen after the cart addition?

# A cart is considered converted only when the recorded
# transaction occurred after the recorded add-to-cart event.
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
# 4. CLASSIFY CART BEHAVIOR
# ============================================================

# Business Question:
# What happened after a visitor added a product to the cart?

# Start with "Other" for visitor-product combinations that
# did not contain a cart event.
first_events["cart_status"] = "Other"


# A cart is classified as Purchased when a transaction
# occurred after the cart addition.
first_events.loc[
    first_events["cart_to_purchase"],
    "cart_status"
] = "Purchased"


# A cart is classified as Abandoned when:
# 1. A cart event exists, and
# 2. No subsequent transaction is recorded.
first_events.loc[
    first_events["has_cart"]
    &
    ~first_events["cart_to_purchase"],
    "cart_status"
] = "Abandoned"


# ============================================================
# 5. CART OUTCOME SUMMARY
# ============================================================

# Business Question:
# Among all visitor-product pairs that added a product to
# the cart, how many converted and how many were abandoned?

# Keep only visitor-product pairs with a recorded cart event.
cart_users = first_events[
    first_events["has_cart"]
]

cart_outcomes = (
    cart_users["cart_status"]
    .value_counts()
)

print("\n========== CART OUTCOMES ==========")

print(
    cart_outcomes
)


# ============================================================
# 6. CART ABANDONMENT AND PURCHASE RATE
# ============================================================

# Business Question:
# What percentage of recorded cart additions were followed
# by a purchase, and what percentage had no subsequent
# recorded purchase?

total_cart_pairs = len(
    cart_users
)

abandoned_pairs = (
    cart_users["cart_status"]
    .eq("Abandoned")
    .sum()
)

purchased_pairs = (
    cart_users["cart_status"]
    .eq("Purchased")
    .sum()
)


# Calculate the percentage of cart pairs with no subsequent
# recorded transaction.
abandonment_rate = (
    abandoned_pairs
    / total_cart_pairs
    * 100
)


# Calculate the percentage of cart pairs followed by a
# recorded purchase.
purchase_rate = (
    purchased_pairs
    / total_cart_pairs
    * 100
)


print("\n========== CART CONVERSION ==========")

print(
    f"Total cart pairs: "
    f"{total_cart_pairs:,}"
)

print(
    f"Purchased pairs: "
    f"{purchased_pairs:,}"
)

print(
    f"Abandoned pairs: "
    f"{abandoned_pairs:,}"
)

print(
    f"Cart abandonment rate: "
    f"{abandonment_rate:.2f}%"
)

print(
    f"Cart → Purchase rate: "
    f"{purchase_rate:.2f}%"
)


# ============================================================
# 7. CONSISTENCY CHECK
# ============================================================

# Data Quality Question:
# Do the purchased and abandoned cart pairs account for
# every visitor-product pair that had a recorded cart event?

print("\n========== CONSISTENCY CHECK ==========")

print(
    "Purchased + Abandoned = Total Cart Pairs:",
    purchased_pairs + abandoned_pairs
    == total_cart_pairs
)