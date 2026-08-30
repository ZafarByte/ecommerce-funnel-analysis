"""
E-commerce Funnel Drop-off Analysis
File: 09_user_engagement.py

Dataset:
RetailRocket E-commerce Dataset

Purpose:
Analyze visitor engagement and determine whether users who
interact more deeply with the e-commerce platform show higher
observed purchase conversion.

Business Questions:
1. How many events does the typical visitor generate?
2. How many products does each visitor view?
3. Does higher engagement correspond to higher purchase conversion?
4. How does purchase conversion change as the number of product
   views increases?
5. Can visitors be grouped into meaningful engagement segments?
6. Which engagement group has the strongest observed conversion?
7. Is there a relationship between repeated product exploration
   and purchase behavior?

Engagement Definition:
- Low: 1–2 product views
- Medium: 3–5 product views
- High: More than 5 product views

View Band Definition:
- 1–2 views
- 3–5 views
- 6–10 views
- 11–20 views
- 21+ views

Important Interpretation Note:
This analysis identifies an association between engagement and
purchase conversion. It does not prove that increasing the number
of views causes users to purchase.

Data Limitation:
The dataset contains observed events and may not represent the
complete customer journey outside the recorded platform activity.
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

print("Data loaded successfully.")


# ============================================================
# 2. CREATE EVENT FLAGS
# ============================================================

# Convert event types into binary indicators.
#
# These flags make it easier to aggregate user behavior
# at the visitor level.

df["is_view"] = (
    df["event"] == "view"
).astype(int)

df["is_cart"] = (
    df["event"] == "addtocart"
).astype(int)

df["is_purchase"] = (
    df["event"] == "transaction"
).astype(int)


# ============================================================
# 3. CREATE VISITOR-LEVEL BEHAVIOR SUMMARY
# ============================================================

# Business Question:
# What does the overall behavior of each visitor look like?

# Aggregate event activity for every visitor.
visitor_summary = (
    df.groupby("visitorid")
      .agg(
          total_events=(
              "event",
              "count"
          ),

          total_views=(
              "is_view",
              "sum"
          ),

          total_cart_events=(
              "is_cart",
              "sum"
          ),

          total_purchases=(
              "is_purchase",
              "sum"
          )
      )
      .reset_index()
)


# ============================================================
# 4. CALCULATE UNIQUE PRODUCTS VIEWED
# ============================================================

# Business Question:
# How many different products did each visitor explore?

# Keep only product-view events.
view_data = df[
    df["event"] == "view"
]


# Count distinct products viewed by each visitor.
unique_products = (
    view_data
    .groupby("visitorid")["itemid"]
    .nunique()
    .reset_index(
        name="unique_products_viewed"
    )
)


# ============================================================
# 5. MERGE UNIQUE PRODUCT DATA
# ============================================================

# Add the number of unique products viewed to the
# visitor-level summary.

visitor_summary = visitor_summary.merge(
    unique_products,
    on="visitorid",
    how="left"
)


# Visitors without a recorded view receive zero for
# unique products viewed.
visitor_summary["unique_products_viewed"] = (
    visitor_summary["unique_products_viewed"]
    .fillna(0)
)


# ============================================================
# 6. DISPLAY VISITOR SUMMARY
# ============================================================

print(
    "\n========== VISITOR SUMMARY =========="
)

print(
    visitor_summary.head(10)
)


# ============================================================
# 7. CREATE PURCHASE FLAG
# ============================================================

# Business Question:
# Which visitors eventually recorded at least one purchase?

# Convert purchase activity into a binary visitor-level flag.
#
# 1 = visitor recorded at least one transaction
# 0 = visitor did not record a transaction

visitor_summary["purchased"] = (
    visitor_summary["total_purchases"] > 0
).astype(int)


print(
    "\n========== PURCHASE DISTRIBUTION =========="
)

print(
    visitor_summary["purchased"].value_counts()
)


# ============================================================
# 8. CREATE ENGAGEMENT SEGMENTS
# ============================================================

# Business Question:
# Can visitors be grouped into low, medium, and high
# engagement segments based on their product-view activity?

def classify_engagement(views):
    """
    Classify visitors based on the number of recorded
    product views.
    """

    if views <= 2:
        return "Low"

    elif views <= 5:
        return "Medium"

    else:
        return "High"


visitor_summary["engagement"] = (
    visitor_summary["total_views"]
    .apply(classify_engagement)
)


print(
    "\n========== ENGAGEMENT DISTRIBUTION =========="
)

print(
    visitor_summary["engagement"]
    .value_counts()
)


# ============================================================
# 9. CONVERSION BY ENGAGEMENT
# ============================================================

# Business Question:
# Do highly engaged visitors have a higher observed purchase
# conversion rate than less engaged visitors?

engagement_analysis = (
    visitor_summary
    .groupby("engagement")
    .agg(
        visitors=(
            "visitorid",
            "count"
        ),

        purchasers=(
            "purchased",
            "sum"
        ),

        avg_views=(
            "total_views",
            "mean"
        ),

        avg_unique_products=(
            "unique_products_viewed",
            "mean"
        ),

        avg_cart_events=(
            "total_cart_events",
            "mean"
        )
    )
    .reset_index()
)


# Calculate the percentage of visitors who recorded
# at least one purchase.
engagement_analysis["conversion_rate"] = (
    engagement_analysis["purchasers"]
    / engagement_analysis["visitors"]
    * 100
)


# Explicitly order engagement levels from Low → Medium → High.
engagement_order = [
    "Low",
    "Medium",
    "High"
]

engagement_analysis["engagement"] = pd.Categorical(
    engagement_analysis["engagement"],
    categories=engagement_order,
    ordered=True
)


engagement_analysis = (
    engagement_analysis
    .sort_values("engagement")
)


print(
    "\n========== CONVERSION BY ENGAGEMENT =========="
)

print(
    engagement_analysis
    .round(2)
    .to_string(index=False)
)


# ============================================================
# 10. CONVERSION BY EXACT VIEW COUNT
# ============================================================

# Business Question:
# How does purchase conversion change as the number of
# product views increases?

# Exclude visitors with zero views because this analysis
# specifically evaluates view-based engagement.
view_count_analysis = (
    visitor_summary[
        visitor_summary["total_views"] > 0
    ]
    .groupby("total_views")
    .agg(
        visitors=(
            "visitorid",
            "count"
        ),

        purchasers=(
            "purchased",
            "sum"
        )
    )
    .reset_index()
)


# Calculate conversion rate for each view count.
view_count_analysis["conversion_rate"] = (
    view_count_analysis["purchasers"]
    / view_count_analysis["visitors"]
    * 100
)


# Only retain view counts with at least 50 visitors.
# This reduces the impact of very small samples that can
# produce unstable conversion percentages.
view_count_analysis = (
    view_count_analysis[
        view_count_analysis["visitors"] >= 50
    ]
)


print(
    "\n========== CONVERSION BY VIEW COUNT =========="
)

print(
    view_count_analysis
    .head(30)
    .round(2)
    .to_string(index=False)
)


# ============================================================
# 11. CREATE VIEW-BASED ENGAGEMENT BANDS
# ============================================================

# Business Question:
# Can we group exact view counts into broader engagement
# bands to make the relationship easier to interpret?

view_engagement = visitor_summary[
    visitor_summary["total_views"] > 0
].copy()


def classify_view_band(views):
    """
    Group visitors into broader view-count bands.
    """

    if views <= 2:
        return "1-2 views"

    elif views <= 5:
        return "3-5 views"

    elif views <= 10:
        return "6-10 views"

    elif views <= 20:
        return "11-20 views"

    else:
        return "21+ views"


view_engagement["view_band"] = (
    view_engagement["total_views"]
    .apply(classify_view_band)
)


# ============================================================
# 12. CONVERSION BY VIEW BAND
# ============================================================

# Business Question:
# Which level of product-view engagement has the strongest
# observed purchase conversion?

view_band_analysis = (
    view_engagement
    .groupby("view_band")
    .agg(
        visitors=(
            "visitorid",
            "count"
        ),

        purchasers=(
            "purchased",
            "sum"
        ),

        avg_views=(
            "total_views",
            "mean"
        ),

        avg_unique_products=(
            "unique_products_viewed",
            "mean"
        )
    )
    .reset_index()
)


# Calculate purchase conversion for each engagement band.
view_band_analysis["conversion_rate"] = (
    view_band_analysis["purchasers"]
    / view_band_analysis["visitors"]
    * 100
)


# Keep the engagement bands in logical order.
view_order = [
    "1-2 views",
    "3-5 views",
    "6-10 views",
    "11-20 views",
    "21+ views"
]


view_band_analysis["view_band"] = pd.Categorical(
    view_band_analysis["view_band"],
    categories=view_order,
    ordered=True
)


view_band_analysis = (
    view_band_analysis
    .sort_values("view_band")
)


print(
    "\n========== CONVERSION BY VIEW BAND =========="
)

print(
    view_band_analysis
    .round(2)
    .to_string(index=False)
)