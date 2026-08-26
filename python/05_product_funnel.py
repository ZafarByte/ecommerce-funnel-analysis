import pandas as pd

# Load data
df = pd.read_csv("../data/raw/events.csv")

# Convert timestamp
df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")

# Sort by visitor, product and time
df = df.sort_values(["visitorid", "itemid", "datetime"])

print("Data sorted successfully.")

print("\n========== SAMPLE ==========")

print(
    df[
        ["visitorid", "itemid", "datetime", "event"]
    ].head(20)
)