import pandas as pd

print("Loading parsed logs...")
df = pd.read_csv("data/parsed_logs.csv", parse_dates=["timestamp"])

print("Total rows:", len(df))
print("Total users:", df["user"].nunique())

# Count records per user
user_counts = df["user"].value_counts().reset_index()
user_counts.columns = ["user", "record_count"]

# Keep users with at least 10 records
active_users = user_counts[user_counts["record_count"] >= 10]

print("Users with at least 10 records:", len(active_users))

# Sample 1000 active users
sampled_users = active_users["user"].sample(
    n=min(1000, len(active_users)),
    random_state=42
)

# Keep all rows for those users
sample_df = df[df["user"].isin(sampled_users)].copy()

print("Sample rows:", len(sample_df))
print("Sample users:", sample_df["user"].nunique())

sample_df.to_csv("data/parsed_logs_sample.csv", index=False)
print("Saved to data/parsed_logs_sample.csv")