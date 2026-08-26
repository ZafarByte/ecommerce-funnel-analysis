import pandas as pd

# Load data
df = pd.read_csv("../data/raw/events.csv")

# Convert timestamp
df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")

print("========== BASIC INFORMATION ==========")

print("Rows:", len(df))
print("Columns:", len(df.columns))

print("\nColumn names:")
print(df.columns.tolist())


print("\n========== EVENT DISTRIBUTION ==========")

print(df["event"].value_counts())


print("\n========== UNIQUE USERS ==========")

print("Unique visitors:", df["visitorid"].nunique())


print("\n========== UNIQUE PRODUCTS ==========")

print("Unique products:", df["itemid"].nunique())


print("\n========== MISSING VALUES ==========")

print(df.isnull().sum())


print("\n========== DATE RANGE ==========")

print("Start:", df["datetime"].min())
print("End:", df["datetime"].max())


print("\n========== DUPLICATES ==========")

print("Duplicate rows:", df.duplicated().sum())