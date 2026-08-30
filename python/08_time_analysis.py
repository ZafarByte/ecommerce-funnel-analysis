"""
E-commerce Funnel Drop-off Analysis
File: 08_time_analysis.py

Dataset:
RetailRocket E-commerce Dataset

Purpose:
Analyze e-commerce activity and funnel conversion across
different dates, days of the week, and hours of the day.

Business Questions:
1. What period of time does the dataset cover?
2. How does event activity change from day to day?
3. How many unique visitors interact with the platform each day?
4. Which days of the week have the highest user activity?
5. Which hours of the day have the highest user activity?
6. Which days have the strongest funnel conversion?
7. Which hours have the strongest View → Purchase conversion?
8. When might marketing or growth teams find the highest-
   performing periods of user activity?

Important Interpretation Note:
High traffic volume does not necessarily mean high conversion.
This analysis therefore examines both:
- User/event volume
- Funnel conversion rates

Data Limitation:
The timestamps represent recorded events in the dataset.
They should be interpreted as observed platform activity rather
than a complete representation of all customer behavior.
"""

import pandas as pd


# ============================================================
# 1. LOAD DATA AND CREATE TIME FEATURES
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

# Create time dimensions that will be used for temporal analysis.
df["date"] = df["datetime"].dt.date

df["day_of_week"] = (
    df["datetime"].dt.day_name()
)

df["hour"] = (
    df["datetime"].dt.hour
)


print("Data loaded successfully.")


# ============================================================
# 2. DATASET DATE RANGE
# ============================================================

# Business Question:
# What period of time is covered by the available event data?

print("\n========== DATE RANGE ==========")

print(
    "Start:",
    df["datetime"].min()
)

print(
    "End:",
    df["datetime"].max()
)


# ============================================================
# 3. DAILY EVENT VOLUME
# ============================================================

# Business Question:
# How does the volume of views, cart additions, and
# transactions change from day to day?

# Count the number of recorded events for each date and event type.
daily_events = (
    df.groupby(
        [
            "date",
            "event"
        ]
    )
    .size()
    .unstack(
        fill_value=0
    )
)

print(
    "\n========== DAILY EVENT VOLUME =========="
)

print(
    daily_events.head(10)
)


# ============================================================
# 4. DAILY UNIQUE USERS
# ============================================================

# Business Question:
# How many unique visitors interacted with the platform
# at each stage on each day?

# Count unique visitors instead of raw events so that repeated
# actions from the same visitor do not inflate daily user counts.
daily_users = (
    df.groupby(
        [
            "date",
            "event"
        ]
    )["visitorid"]
    .nunique()
    .unstack(
        fill_value=0
    )
)

print(
    "\n========== DAILY UNIQUE USERS =========="
)

print(
    daily_users.head(10)
)


# ============================================================
# 5. USER ACTIVITY BY DAY OF WEEK
# ============================================================

# Business Question:
# Which days of the week have the highest number of unique
# visitors at each funnel stage?

weekday_users = (
    df.groupby(
        [
            "day_of_week",
            "event"
        ]
    )["visitorid"]
    .nunique()
    .unstack(
        fill_value=0
    )
)


# Reorder the days chronologically instead of alphabetically.
weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weekday_users = weekday_users.reindex(
    weekday_order
)


print(
    "\n========== UNIQUE USERS BY DAY OF WEEK =========="
)

print(
    weekday_users
)


# ============================================================
# 6. USER ACTIVITY BY HOUR
# ============================================================

# Business Question:
# During which hours of the day are users most active?

hourly_users = (
    df.groupby(
        [
            "hour",
            "event"
        ]
    )["visitorid"]
    .nunique()
    .unstack(
        fill_value=0
    )
)

print(
    "\n========== UNIQUE USERS BY HOUR =========="
)

print(
    hourly_users
)


# ============================================================
# 7. DAY-OF-WEEK CONVERSION
# ============================================================

# Business Question:
# Which days of the week have the strongest funnel conversion?

# Use the unique-user counts from the weekday analysis to
# calculate stage-to-stage conversion rates.

weekday_conversion = (
    weekday_users.copy()
)


# Percentage of viewers who also recorded an add-to-cart event.
weekday_conversion["view_to_cart"] = (
    weekday_conversion["addtocart"]
    / weekday_conversion["view"]
    * 100
)


# Percentage of cart users who also recorded a transaction.
weekday_conversion["cart_to_purchase"] = (
    weekday_conversion["transaction"]
    / weekday_conversion["addtocart"]
    * 100
)


# Percentage of viewers who also recorded a transaction.
weekday_conversion["view_to_purchase"] = (
    weekday_conversion["transaction"]
    / weekday_conversion["view"]
    * 100
)


print(
    "\n========== DAY-OF-WEEK CONVERSION =========="
)

print(
    weekday_conversion[
        [
            "view_to_cart",
            "cart_to_purchase",
            "view_to_purchase"
        ]
    ]
    .round(2)
)


# ============================================================
# 8. HOURLY CONVERSION
# ============================================================

# Business Question:
# Which hours of the day have the strongest funnel conversion?

hourly_conversion = (
    hourly_users.copy()
)


# Calculate View → Cart conversion by hour.
hourly_conversion["view_to_cart"] = (
    hourly_conversion["addtocart"]
    / hourly_conversion["view"]
    * 100
)


# Calculate Cart → Purchase conversion by hour.
hourly_conversion["cart_to_purchase"] = (
    hourly_conversion["transaction"]
    / hourly_conversion["addtocart"]
    * 100
)


# Calculate overall View → Purchase conversion by hour.
hourly_conversion["view_to_purchase"] = (
    hourly_conversion["transaction"]
    / hourly_conversion["view"]
    * 100
)


print(
    "\n========== HOURLY CONVERSION =========="
)

print(
    hourly_conversion[
        [
            "view_to_cart",
            "cart_to_purchase",
            "view_to_purchase"
        ]
    ]
    .round(2)
)


# ============================================================
# 9. IDENTIFY BEST-PERFORMING HOURS
# ============================================================

# Business Question:
# Which hours have the highest observed View → Purchase
# conversion?

# Sort hours by overall funnel conversion.
best_hours = (
    hourly_conversion
    .sort_values(
        "view_to_purchase",
        ascending=False
    )
)


print(
    "\n========== TOP HOURS BY VIEW → PURCHASE =========="
)

print(
    best_hours[
        [
            "view",
            "addtocart",
            "transaction",
            "view_to_cart",
            "cart_to_purchase",
            "view_to_purchase"
        ]
    ]
    .head(10)
    .round(2)
)


# ============================================================
# 10. IDENTIFY BEST-PERFORMING DAYS
# ============================================================

# Business Question:
# Which days of the week have the highest observed
# View → Purchase conversion?

# Sort weekdays by overall funnel conversion.
best_days = (
    weekday_conversion
    .sort_values(
        "view_to_purchase",
        ascending=False
    )
)


print(
    "\n========== DAYS BY VIEW → PURCHASE =========="
)

print(
    best_days[
        [
            "view",
            "addtocart",
            "transaction",
            "view_to_cart",
            "cart_to_purchase",
            "view_to_purchase"
        ]
    ]
    .round(2)
)