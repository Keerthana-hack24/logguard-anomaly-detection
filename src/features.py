import pandas as pd
import numpy as np

def calculate_entropy(series):
    clean_values = [str(x) for x in series if pd.notna(x)]
    if len(clean_values) == 0:
        return 0
    probabilities = pd.Series(clean_values).value_counts(normalize=True)
    entropy = -np.sum(probabilities * np.log2(probabilities + 1e-9))
    return entropy

df = pd.read_csv("data/parsed_logs_sample.csv", parse_dates=["timestamp"])

#Creating different columns for new user_features.csv:
grouped = df.groupby("user")
login_attempt_count = grouped.size().reset_index(name="login_attempt_count")

failed_login_count=grouped["success"].apply(lambda x: (x==0).sum()).reset_index(name="failed_login_count")

success_login_count=grouped["success"].apply(lambda x: (x==1).sum()).reset_index(name="success_login_count")

unique_ip_count= grouped["ip"].nunique().reset_index(name="unique_ip_count")

unique_country_count= grouped["country"].nunique().reset_index(name="unique_country_count")

unique_device_count=grouped["device"].nunique().reset_index(name="unique_device_count")

avg_login_hour=grouped["hour"].mean().reset_index(name="avg_login_hour")

std_login_hour = grouped["hour"].std().reset_index(name="std_login_hour")

first_login_time = grouped["timestamp"].min().reset_index(name="first_login_time")

last_login_time = grouped["timestamp"].max().reset_index(name="last_login_time")

user_features = login_attempt_count

user_features = user_features.merge(failed_login_count, on="user")
user_features = user_features.merge(success_login_count, on="user")
user_features = user_features.merge(unique_ip_count, on="user")
user_features = user_features.merge(unique_country_count, on="user")
user_features = user_features.merge(unique_device_count, on="user")
user_features = user_features.merge(avg_login_hour, on="user")
user_features = user_features.merge(std_login_hour, on="user")
user_features = user_features.merge(first_login_time, on="user")
user_features = user_features.merge(last_login_time, on="user")

#Failed login ratio:
user_features["failed_login_ratio"] = (user_features["failed_login_count"]/user_features["login_attempt_count"])

# Activity span in hours:
time_difference = user_features["last_login_time"] - user_features["first_login_time"]
user_features["activity_span_hours"] = time_difference.dt.total_seconds()/3600

# Fill missing values:
user_features["activity_span_hours"] = user_features["activity_span_hours"].fillna(0)
user_features["std_login_hour"] = user_features["std_login_hour"].fillna(0)

# Login rate per hour:
user_features["login_rate_per_hour"] = (user_features["login_attempt_count"] / (user_features["activity_span_hours"] + 1))

# IP entropy
ip_entropy = grouped["ip"].apply(calculate_entropy).reset_index(name="ip_entropy")

# Country entropy
country_entropy = grouped["country"].apply(calculate_entropy).reset_index(name="country_entropy")

# Device entropy
device_entropy = grouped["device"].apply(calculate_entropy).reset_index(name="device_entropy")

user_features = user_features.merge(ip_entropy, on="user")
user_features = user_features.merge(country_entropy, on="user")
user_features = user_features.merge(device_entropy, on="user")

user_features["ip_entropy"] = user_features["ip_entropy"].clip(lower=0)
user_features["country_entropy"] = user_features["country_entropy"].clip(lower=0)
user_features["device_entropy"] = user_features["device_entropy"].clip(lower=0)

user_features.to_csv("data/user_features.csv", index=False)

print("Feature engineering complete")
print(user_features.head())
print("Saved to data/user_features.csv")