"""
E-commerce Funnel Drop-off Analysis
File: 01_data_understanding.py

Dataset:
RetailRocket E-commerce Dataset

Purpose:
Perform initial data understanding and identify the structure,
size, event types, missing values, and time period of the dataset.

Business Questions:
1. What types of user events are present in the dataset?
2. How many unique visitors and products are represented?
3. Are there missing values that need to be considered?
4. What time period does the dataset cover?
5. Can the raw timestamp be converted into useful date/time
   dimensions for further analysis?
"""

import pandas as pd


# ============================================================
# 1. LOAD DATA
# ============================================================

# Load the raw RetailRocket event dataset.
df = pd.read_csv("../data/raw/events.csv")


# ============================================================
# 2. UNDERSTAND EVENT DISTRIBUTION
# ============================================================

# Business Question:
# What types of interactions are recorded in the dataset,
# and how frequently does each event occur?

print("========== EVENT DISTRIBUTION ==========")
print(df["event"].value_counts())


# ============================================================
# 3. COUNT UNIQUE VISITORS
# ============================================================

# Business Question:
# How many unique visitors are represented in the dataset?

print("\n========== UNIQUE VISITORS ==========")
print(df["visitorid"].nunique())


# ============================================================
# 4. COUNT UNIQUE PRODUCTS
# ============================================================

# Business Question:
# How many unique products are represented in the dataset?

print("\n========== UNIQUE PRODUCTS ==========")
print(df["itemid"].nunique())


# ============================================================
# 5. CHECK MISSING VALUES
# ============================================================

# Business Question:
# Which columns contain missing values, and how much missing
# data will need to be considered during the analysis?

print("\n========== MISSING VALUES ==========")
print(df.isnull().sum())


# ============================================================
# 6. CONVERT TIMESTAMP
# ============================================================

# The original timestamp is stored as Unix time in milliseconds.
# Convert it into a pandas datetime column so that it can be
# used for chronological and time-based analysis.

df["datetime"] = pd.to_datetime(
    df["timestamp"],
    unit="ms"
)


# ============================================================
# 7. INITIAL DATA INSPECTION
# ============================================================

# Business Question:
# What does the dataset look like after loading and timestamp
# conversion, and how large is the dataset?

print("\n========== FIRST 5 ROWS ==========")
print(df.head())

print("\n========== DATASET SHAPE ==========")
print(df.shape)

print("\n========== DATASET INFORMATION ==========")
print(df.info())


# ============================================================
# 8. VERIFY TIMESTAMP CONVERSION
# ============================================================

# Business Question:
# Was the Unix timestamp converted correctly into a readable
# datetime value?

print("\n========== TIMESTAMP CONVERSION CHECK ==========")

print(
    df[
        ["timestamp", "datetime"]
    ].head()
)


# ============================================================
# 9. CREATE TIME DIMENSIONS
# ============================================================

# Create additional time-related columns that will be useful
# for daily, monthly, weekday, and hourly analysis.

df["date"] = df["datetime"].dt.date

df["month"] = df["datetime"].dt.to_period("M")

df["day_of_week"] = df["datetime"].dt.day_name()

df["hour"] = df["datetime"].dt.hour


# Business Question:
# Can the timestamp be transformed into useful time dimensions
# for identifying traffic and conversion patterns?

print("\n========== TIME DIMENSIONS ==========")

print(
    df[
        [
            "datetime",
            "date",
            "month",
            "day_of_week",
            "hour"
        ]
    ].head(10)
)


# ============================================================
# 10. IDENTIFY DATASET TIME RANGE
# ============================================================

# Business Question:
# What period of time is covered by the available event data?

print("\n========== DATASET TIME RANGE ==========")

print("First date:", df["datetime"].min())
print("Last date:", df["datetime"].max())