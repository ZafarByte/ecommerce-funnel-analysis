import pandas as pd

# Load data
df = pd.read_csv("../data/raw/events.csv")

# Convert timestamp
df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")

# --------------------------------------------------
# 1. Unique users at each funnel stage
# --------------------------------------------------

funnel_users = (
    df.groupby("event")["visitorid"]
      .nunique()
      .sort_values(ascending=False)
)

print("========== UNIQUE USERS BY EVENT ==========")
print(funnel_users)