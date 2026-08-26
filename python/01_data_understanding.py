import pandas as pd

df = pd.read_csv("../data/raw/events.csv")

print(df["event"].value_counts())
print(df["visitorid"].nunique())
print(df["itemid"].nunique())

print(df.isnull().sum())


#Convert timestamp
df["datetime"] = pd.to_datetime(
    df["timestamp"],
    unit="ms"
)
#checking the first few rows, shape and info of the dataframe
print(df.head())
print(df.shape)
print(df.info())
#printing the first few rows of the timestamp and datetime columns to verify the conversion
print(df[["timestamp", "datetime"]].head())
#converting the datetime column to date, month, day of week and hour columns
df["date"] = df["datetime"].dt.date
df["month"] = df["datetime"].dt.to_period("M")
df["day_of_week"] = df["datetime"].dt.day_name()
df["hour"] = df["datetime"].dt.hour

print(df[[
    "datetime",
    "date",
    "month",
    "day_of_week",
    "hour"
]].head(10))

print("First date:", df["datetime"].min())
print("Last date:", df["datetime"].max())
