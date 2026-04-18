from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

df= pd.read_csv("data/user_features.csv")

feature_columns = ["login_attempt_count","failed_login_count","success_login_count","unique_ip_count","unique_country_count","unique_device_count","avg_login_hour","std_login_hour","failed_login_ratio","activity_span_hours","login_rate_per_hour","ip_entropy","country_entropy","device_entropy"]

x = df[feature_columns]

model = IsolationForest(n_estimators=100,contamination=0.05,random_state=42)

print("Training model...")
model.fit(x)
print("Model training complete!")

predictions = model.predict(x)
df["anomaly_label"] = predictions

scores = model.decision_function(x)

df["anomaly_score"]=scores

#Converting the anomaly_score to a scale of 0-100:

df["raw_risk"] = -df["anomaly_score"]

scaler = MinMaxScaler(feature_range=(0,100))
df["risk_score"]=scaler.fit_transform(df[["raw_risk"]]) #as maxminscaler works on 2D data
df["risk_score"]=df["risk_score"].round(2)

def get_risk_level(score):
    if 0<=score<=39:
        return "Low"
    elif 40<=score<=69:
        return "Medium"
    else:
        return "High"

df["risk_level"] = df["risk_score"].apply(get_risk_level)

df = df.sort_values("risk_score",ascending=False)

df.to_csv("data/model_results.csv", index=False)