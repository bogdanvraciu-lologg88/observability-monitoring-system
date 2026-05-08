import json
import os

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from streamlit_autorefresh import st_autorefresh

st.set_page_config(
    page_title="Observability Dashboard",
    layout="wide"
)

st.title("📊 Observability Monitoring Dashboard")
st_autorefresh(interval=30000, key="dashboardrefresh")
st.markdown("Simple monitoring dashboard for service metrics and alerts")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
HISTORY_FILE = os.path.join(BASE_DIR, "data", "history.json")


try:
    with open(HISTORY_FILE, "r") as file:
        history = json.load(file)

except Exception as e:
    st.error(f"Error loading history file: {e}")
    history = []


if not history:
    st.warning("No monitoring data available yet.")
    st.stop()


df = pd.DataFrame(history)

df["timestamp"] = pd.to_datetime(df["timestamp"])


st.sidebar.header("Dashboard Filters")

services = df["service"].unique()

selected_service = st.sidebar.selectbox(
    "Select Service",
    services
)


filtered_df = df[df["service"] == selected_service]


latest_response = filtered_df.iloc[-1]["response_time"]

avg_response = round(filtered_df["response_time"].mean(), 3)

max_response = round(filtered_df["response_time"].max(), 3)


col1, col2, col3 = st.columns(3)

col1.metric("Latest Response", f"{latest_response}s")
col2.metric("Average Response", f"{avg_response}s")
col3.metric("Max Response", f"{max_response}s")


st.subheader("📈 Response Time History")

fig, ax = plt.subplots(figsize=(10, 4))

ax.plot(
    filtered_df["timestamp"],
    filtered_df["response_time"]
)

ax.set_xlabel("Timestamp")
ax.set_ylabel("Response Time (s)")

st.pyplot(fig)


st.subheader("📝 Recent Monitoring Events")

st.dataframe(
    filtered_df.tail(10),
    use_container_width=True
)


st.subheader("🚦 Service Health")

if latest_response < 1:
    st.success("Service operating normally")

elif latest_response < 3:
    st.warning("Service latency elevated")

else:
    st.error("Potential performance issue detected")