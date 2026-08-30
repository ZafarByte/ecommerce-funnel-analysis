"""
E-commerce Funnel Drop-off Analysis
File: 03_funnel_analysis.py

Dataset:
RetailRocket E-commerce Dataset

Purpose:
Calculate the basic e-commerce funnel using unique visitors
at each event stage and identify where the largest percentage
of users drop off.

Business Questions:
1. How many unique visitors reached each funnel stage?
2. What percentage of visitors moved from viewing a product
   to adding it to the cart?
3. What percentage of cart users proceeded to purchase?
4. What percentage of viewers ultimately became purchasers?
5. Which funnel stage has the largest drop-off?

Note:
This is a basic user-level funnel. It does not verify whether
the events occurred in chronological order.
A sequential funnel is analyzed separately.
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
# 2. UNIQUE USERS AT EACH FUNNEL STAGE
# ============================================================

# Business Question:
# How many unique visitors reached each stage of the
# e-commerce journey?
#
# The three funnel stages are:
# View → Add to Cart → Purchase
#
# nunique() is used because the same visitor can generate
# multiple events.

funnel_users = (
    df.groupby("event")["visitorid"]
      .nunique()
)


# Retrieve the number of unique visitors at each stage.
# .get() prevents an error if an expected event is missing.

view_users = funnel_users.get(
    "view",
    0
)

cart_users = funnel_users.get(
    "addtocart",
    0
)

purchase_users = funnel_users.get(
    "transaction",
    0
)


print("========== FUNNEL USERS ==========")

print(
    f"View users:        {view_users:,}"
)

print(
    f"Add-to-cart users: {cart_users:,}"
)

print(
    f"Purchase users:    {purchase_users:,}"
)


# ============================================================
# 3. CONVERSION RATES
# ============================================================

# Business Question:
# What percentage of users move from one funnel stage
# to the next?
#
# These calculations provide a basic user-level view of
# funnel performance.

view_to_cart = (
    cart_users / view_users
) * 100

cart_to_purchase = (
    purchase_users / cart_users
) * 100

view_to_purchase = (
    purchase_users / view_users
) * 100


print("\n========== CONVERSION RATES ==========")

print(
    f"View → Add to Cart: "
    f"{view_to_cart:.2f}%"
)

print(
    f"Add to Cart → Purchase: "
    f"{cart_to_purchase:.2f}%"
)

print(
    f"View → Purchase: "
    f"{view_to_purchase:.2f}%"
)


# ============================================================
# 4. DROP-OFF RATES
# ============================================================

# Business Question:
# What percentage of users are lost between each funnel stage?
#
# Drop-off represents the percentage of users who did not
# progress to the next stage.

view_to_cart_dropoff = (
    100 - view_to_cart
)

cart_to_purchase_dropoff = (
    100 - cart_to_purchase
)


print("\n========== DROP-OFF RATES ==========")

print(
    f"View → Add to Cart Drop-off: "
    f"{view_to_cart_dropoff:.2f}%"
)

print(
    f"Add to Cart → Purchase Drop-off: "
    f"{cart_to_purchase_dropoff:.2f}%"
)