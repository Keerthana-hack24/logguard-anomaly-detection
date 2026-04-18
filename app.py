import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

st.set_page_config(
    page_title="LogGuard Dashboard",
    layout="wide"
)

st.markdown("""
<style>
    /* ── Base & background ── */
    .stApp {
        background-color: #0d1117;
        color: #e6edf3;
    }

    /* ── Main content area ── */
    .block-container {
        background-color: #0d1117;
        padding-top: 2rem;
    }

    /* ── Title ── */
    h1 {
        font-family: 'Courier New', monospace;
        color: #f0883e !important;
        letter-spacing: 2px;
        font-size: 1.8rem !important;
        border-bottom: 2px solid #f0883e44;
        padding-bottom: 0.5rem;
        margin-bottom: 0.25rem !important;
    }

    /* ── Subheadings ── */
    h2, h3 {
        font-family: 'Courier New', monospace;
        color: #58a6ff !important;
        letter-spacing: 1px;
        font-size: 1.1rem !important;
        border-left: 3px solid #f0883e;
        padding-left: 0.6rem;
        margin-top: 1.5rem !important;
    }

    /* ── Metric cards ── */
    [data-testid="stMetric"] {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 1rem 1.2rem;
        box-shadow: 0 0 12px #f0883e22;
    }
    [data-testid="stMetricLabel"] {
        color: #8b949e !important;
        font-family: 'Courier New', monospace;
        font-size: 0.75rem !important;
        letter-spacing: 1px;
        text-transform: uppercase;
    }
    [data-testid="stMetricValue"] {
        color: #f0883e !important;
        font-family: 'Courier New', monospace;
        font-size: 2rem !important;
    }

    /* ── Dataframe ── */
    [data-testid="stDataFrame"] {
        border: 1px solid #30363d;
        border-radius: 6px;
        overflow: hidden;
    }

    /* ── Selectbox ── */
    [data-testid="stSelectbox"] label {
        color: #8b949e !important;
        font-family: 'Courier New', monospace;
        font-size: 0.8rem;
    }

    /* ── Divider ── */
    hr {
        border-color: #21262d !important;
        margin: 1.5rem 0 !important;
    }

    /* ── Body text / write ── */
    p, .stMarkdown p {
        color: #c9d1d9;
        font-family: 'Courier New', monospace;
        font-size: 0.88rem;
    }

    /* ── Risk badge inline text ── */
    .risk-high   { color: #ff6b6b; font-weight: bold; }
    .risk-medium { color: #f0883e; font-weight: bold; }
    .risk-low    { color: #3fb950; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("⚡ LOG-GUARD — AI Security Anomaly Detection")
st.write("Suspicious login behavior detected via Isolation Forest and behavioral feature engineering.")


df = pd.read_csv("data/model_results.csv")


total_users       = len(df)
anomalies_detected = (df["anomaly_label"] == -1).sum()
high_risk_users   = (df["risk_level"] == "High").sum()
average_risk_score = round(df["risk_score"].mean(), 2)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Users Monitored", total_users)
with col2:
    st.metric("Anomalies Detected", anomalies_detected)
with col3:
    st.metric("High Risk Users", high_risk_users)
with col4:
    st.metric("Avg Risk Score", average_risk_score)

st.divider()


# Suspicious users table:
st.subheader("Suspicious Users Overview")

table_columns = [
    "user",
    "anomaly_label",
    "risk_score",
    "risk_level",
    "failed_login_ratio",
    "unique_ip_count",
    "unique_country_count",
    "unique_device_count"
]

st.dataframe(
    df[table_columns].sort_values("risk_score", ascending=False),
    use_container_width=True
)

st.divider()


# User investigation section:
st.subheader("Investigate a User")

selected_user = st.selectbox(
    "Select a user to investigate",
    df["user"].sort_values().unique()
)

selected_row = df[df["user"] == selected_user].iloc[0]


# Flagging logic — calibrated for 5% anomaly rate (50/1000)
# Thresholds use percentile-based reasoning:
#   only the truly outlying users should trigger multiple flags
def generate_reasons(row):
    reasons = []

    # Top 10% of failed login ratios
    if row["failed_login_ratio"] > 0.7:
        reasons.append("Very high failed login ratio (>70%)")

    # More than 5 IPs is genuinely suspicious
    if row["unique_ip_count"] > 5:
        reasons.append("Logins from many distinct IP addresses (>5)")

    # Multiple countries is a strong signal
    if row["unique_country_count"] > 2:
        reasons.append("Logins originating from 3+ different countries")

    # More than 3 device types is unusual
    if row["unique_device_count"] > 3:
        reasons.append("More than 3 different device types used")

    # Unusually high login rate — raised from 0.15
    if row["login_rate_per_hour"] > 0.5:
        reasons.append("Abnormally high login frequency (>0.5/hr)")

    # IP entropy raised — only extreme cases
    if row["ip_entropy"] > 2.0:
        reasons.append("Extremely high IP address diversity")

    # Country entropy raised
    if row["country_entropy"] > 1.0:
        reasons.append("High geographic spread of login origins")

    # Device entropy raised
    if row["device_entropy"] > 1.0:
        reasons.append("High diversity across device types")

    if len(reasons) == 0:
        reasons.append("No strong behavioral risk indicators — anomaly driven by model score")

    return reasons


reasons = generate_reasons(selected_row)


# Selected user details:
detail_col1, detail_col2 = st.columns([1, 2])

risk_color = {
    "High": "#ff6b6b",
    "Medium": "#f0883e",
    "Low": "#3fb950"
}.get(selected_row["risk_level"], "#8b949e")

with detail_col1:
    st.markdown(f"**User:** `{selected_row['user']}`")
    st.markdown(f"**Anomaly Label:** `{selected_row['anomaly_label']}`")
    st.markdown(f"**Anomaly Score:** `{round(selected_row['anomaly_score'], 4)}`")
    st.markdown(f"**Risk Score:** `{selected_row['risk_score']}`")
    st.markdown(
        f"**Risk Level:** <span style='color:{risk_color}; font-weight:bold;'>{selected_row['risk_level']}</span>",
        unsafe_allow_html=True
    )

with detail_col2:
    st.markdown("**Reasons Flagged:**")
    for reason in reasons:
        st.markdown(f"- {reason}")


# Feature table for selected user:
st.markdown("**Behavior Features for Selected User**")

feature_view_columns = [
    "login_attempt_count",
    "failed_login_count",
    "success_login_count",
    "failed_login_ratio",
    "unique_ip_count",
    "unique_country_count",
    "unique_device_count",
    "avg_login_hour",
    "std_login_hour",
    "activity_span_hours",
    "login_rate_per_hour",
    "ip_entropy",
    "country_entropy",
    "device_entropy"
]

st.dataframe(
    selected_row[feature_view_columns].to_frame(name="value"),
    use_container_width=True
)

st.divider()


# Shared chart style:
CHART_BG    = "#0d1117"
AXES_BG     = "#161b22"
TEXT_COLOR  = "#c9d1d9"
ACCENT      = "#f0883e"
ACCENT2     = "#58a6ff"
GRID_COLOR  = "#21262d"

def style_ax(ax, fig):
    fig.patch.set_facecolor(CHART_BG)
    ax.set_facecolor(AXES_BG)
    ax.tick_params(colors=TEXT_COLOR)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.title.set_color(TEXT_COLOR)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)
    ax.yaxis.grid(True, color=GRID_COLOR, linewidth=0.5)
    ax.set_axisbelow(True)



# Chart 1: Risk score distribution:
st.subheader("Risk Score Distribution")

fig1, ax1 = plt.subplots(figsize=(10, 4))
n, bins, patches = ax1.hist(df["risk_score"], bins=20, color=ACCENT2, edgecolor=CHART_BG, linewidth=0.5)

# Gradient-color the bars by height
norm = plt.Normalize(n.min(), n.max())
for count, patch in zip(n, patches):
    patch.set_facecolor(plt.cm.cool(norm(count)))

ax1.set_xlabel("Risk Score")
ax1.set_ylabel("Number of Users")
ax1.set_title("Distribution of Risk Scores Across All Users")
style_ax(ax1, fig1)
st.pyplot(fig1)


# Chart 2: Top 10 risky users:
st.subheader("Top 10 Risky Users")

top_10 = df.sort_values("risk_score", ascending=False).head(10)

fig2, ax2 = plt.subplots(figsize=(10, 5))

bar_colors = [ACCENT if v > df["risk_score"].quantile(0.95) else ACCENT2 for v in top_10["risk_score"]]
bars = ax2.bar(top_10["user"], top_10["risk_score"], color=bar_colors, edgecolor=CHART_BG, linewidth=0.5)

# Value labels on bars
for bar in bars:
    ax2.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.3,
        f"{bar.get_height():.1f}",
        ha="center", va="bottom", color=TEXT_COLOR, fontsize=8, fontfamily="monospace"
    )

ax2.set_xlabel("User")
ax2.set_ylabel("Risk Score")
ax2.set_title("Top 10 Users by Risk Score")
plt.xticks(rotation=45, ha="right")
style_ax(ax2, fig2)
st.pyplot(fig2)


