import pandas as pd

# Load dataset
df = pd.read_csv("data/rba-dataset.csv")

# Convert timestamp
df["timestamp"] = pd.to_datetime(df["timestamp"],dayfirst=True,errors="coerce")
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek

# Convert success True/False → 1/0
df["success"] = df["success"].astype(int)

# Convert user IDs into simple readable IDs
df["user"] = df["user"].astype(str)
df["user"] = "user_" + pd.factorize(df["user"])[0].astype(str)

# Extract useful time features
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek

# Save cleaned dataset
df.to_csv("data/parsed_logs.csv", index=False)

print("Parsing complete")
print(df.head())