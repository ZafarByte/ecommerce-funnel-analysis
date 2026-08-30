"""
E-commerce Funnel Drop-off Analysis
File: 02_data_validation.py

Dataset:
RetailRocket E-commerce Dataset

Purpose:
Validate the structure and quality of the raw e-commerce
event data before performing funnel and behavioral analysis.

Business Questions:
1. How large is the dataset?
2. What columns and event types are available?
3. How many unique visitors and products are represented?
4. Which columns contain missing values?
5. What time period does the dataset cover?
6. Are there duplicate records that could affect the analysis?
"""

import pandas as pd


# ============================================================
# 1. LOAD DATA
# ============================================================

# Load the raw RetailRocket event dataset.
df = pd.read_csv("../data/raw/events.csv")


# ============================================================
# 2. CONVERT TIMESTAMP
# ============================================================

# Convert Unix timestamp stored in milliseconds into a
# readable datetime column for time-based validation.
df["datetime"] = pd.to_datetime(
    df["timestamp"],
    unit="ms"
)


# ============================================================
# 3. BASIC DATASET INFORMATION
# ============================================================

# Business Question:
# How large is the dataset and how many columns are available?

print("========== BASIC INFORMATION ==========")

print("Rows:", len(df))

print("Columns:", len(df.columns))

print("\nColumn names:")

print(df.columns.tolist())


# ============================================================
# 4. EVENT DISTRIBUTION
# ============================================================

# Business Question:
# What types of user interactions are recorded, and how
# frequently does each event occur?

print("\n========== EVENT DISTRIBUTION ==========")

print(
    df["event"].value_counts()
)


# ============================================================
# 5. UNIQUE USERS
# ============================================================

# Business Question:
# How many unique visitors are represented in the dataset?

print("\n========== UNIQUE USERS ==========")

print(
    "Unique visitors:",
    df["visitorid"].nunique()
)


# ============================================================
# 6. UNIQUE PRODUCTS
# ============================================================

# Business Question:
# How many unique products are represented in the dataset?

print("\n========== UNIQUE PRODUCTS ==========")

print(
    "Unique products:",
    df["itemid"].nunique()
)


# ============================================================
# 7. MISSING VALUE CHECK
# ============================================================

# Business Question:
# Which columns contain missing values that could affect
# downstream analysis?

print("\n========== MISSING VALUES ==========")

print(
    df.isnull().sum()
)


# ============================================================
# 8. DATE RANGE VALIDATION
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
# 9. DUPLICATE RECORD CHECK
# ============================================================

# Business Question:
# Are there completely duplicated rows that could result in
# double-counting events or distort funnel metrics?

print("\n========== DUPLICATES ==========")

print(
    "Duplicate rows:",
    df.duplicated().sum()
)