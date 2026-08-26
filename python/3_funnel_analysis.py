#Funnel Conversion & Drop-off Analysis.
import pandas as pd

# Load data
df = pd.read_csv("../data/raw/events.csv")

# Convert timestamp
df["datetime"] = pd.to_datetime(df["timestamp"], unit="ms")


# ==========================================
# 1. UNIQUE USERS AT EACH FUNNEL STAGE
# ==========================================

funnel_users = (
    df.groupby("event")["visitorid"]
      .nunique()
)

view_users = funnel_users.get("view", 0)
cart_users = funnel_users.get("addtocart", 0)
purchase_users = funnel_users.get("transaction", 0)


print("========== FUNNEL USERS ==========")

print(f"View users:        {view_users:,}")
print(f"Add-to-cart users: {cart_users:,}")
print(f"Purchase users:    {purchase_users:,}")


# ==========================================
# 2. CONVERSION RATES
# ==========================================

view_to_cart = (cart_users / view_users) * 100
cart_to_purchase = (purchase_users / cart_users) * 100
view_to_purchase = (purchase_users / view_users) * 100


print("\n========== CONVERSION RATES ==========")

print(f"View → Add to Cart: {view_to_cart:.2f}%")
print(f"Add to Cart → Purchase: {cart_to_purchase:.2f}%")
print(f"View → Purchase: {view_to_purchase:.2f}%")


# ==========================================
# 3. DROP-OFF RATES
# ==========================================

view_to_cart_dropoff = 100 - view_to_cart
cart_to_purchase_dropoff = 100 - cart_to_purchase


print("\n========== DROP-OFF RATES ==========")

print(f"View → Add to Cart Drop-off: {view_to_cart_dropoff:.2f}%")
print(f"Add to Cart → Purchase Drop-off: {cart_to_purchase_dropoff:.2f}%")