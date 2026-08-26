import pandas as pd

# Load data
df = pd.read_csv("../data/raw/events.csv")

# Convert timestamp
df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")

# Sort events chronologically for each visitor
df = df.sort_values(["visitorid", "datetime"])

print("Data sorted successfully.")

print("\nFirst 20 events:")
print(df[[
    "visitorid",
    "datetime",
    "event",
    "itemid"
]].head(20))

# First time each visitor performed each event
first_events = (
    df.groupby(["visitorid", "event"])["datetime"]
      .min()
      .unstack()
)

print("\n========== FIRST EVENT TIMESTAMPS ==========")
print(first_events.head())

# Check whether each stage exists
first_events["has_view"] = first_events["view"].notna()
first_events["has_cart"] = first_events["addtocart"].notna()
first_events["has_purchase"] = first_events["transaction"].notna()

# Check chronological progression
first_events["view_to_cart"] = (
    first_events["view"].notna()
    & first_events["addtocart"].notna()
    & (first_events["view"] < first_events["addtocart"])
)

first_events["cart_to_purchase"] = (
    first_events["addtocart"].notna()
    & first_events["transaction"].notna()
    & (first_events["addtocart"] < first_events["transaction"])
)

# Complete sequential funnel
first_events["full_funnel"] = (
    first_events["view_to_cart"]
    & first_events["cart_to_purchase"]
)

print("\n========== SEQUENTIAL FUNNEL ==========")

view_users = first_events["has_view"].sum()

view_to_cart_users = first_events["view_to_cart"].sum()

cart_to_purchase_users = first_events["cart_to_purchase"].sum()

full_funnel_users = first_events["full_funnel"].sum()

print(f"Users who viewed: {view_users:,}")
print(f"Users who viewed → cart: {view_to_cart_users:,}")
print(f"Users who carted → purchased: {cart_to_purchase_users:,}")
print(f"Users completing full funnel: {full_funnel_users:,}")

view_to_cart_rate = (
    view_to_cart_users / view_users * 100
)

cart_to_purchase_rate = (
    cart_to_purchase_users / view_to_cart_users * 100
)

overall_conversion = (
    full_funnel_users / view_users * 100
)

print("\n========== SEQUENTIAL CONVERSION ==========")

print(f"View → Cart: {view_to_cart_rate:.2f}%")
print(f"Cart → Purchase: {cart_to_purchase_rate:.2f}%")
print(f"View → Purchase: {overall_conversion:.2f}%")