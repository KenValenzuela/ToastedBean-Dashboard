# app/pages/4_Daily_Insights.py

import streamlit as st
from utils import fetch_query, rename_columns
import pandas as pd
import plotly.express as px
import altair as alt

# === Page Setup ===
st.set_page_config(page_title="Daily Insights", layout="wide")
st.title("📅 Daily Order Insights")
st.caption("Analyze day-level sales patterns including hourly volume, item performance, and revenue mix.")
st.markdown("---")

# === Load and Prepare Data ===
df = fetch_query("sql/detail_items.sql")
df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce", utc=True)
df = df.dropna(subset=["datetime", "gross_sales"])
df["date"] = df["datetime"].dt.date
df["hour"] = df["datetime"].dt.hour
df["weekday"] = df["datetime"].dt.day_name()

# === Sidebar Filters ===
st.sidebar.header("📂 Filter Options")
available_dates = sorted(df["date"].unique(), reverse=True)
selected_date = st.sidebar.selectbox("Select a Date", available_dates)

card_options = df["card_brand"].dropna().unique()
channel_options = df["channel"].dropna().unique()

selected_cards = st.sidebar.multiselect("Payment Type", card_options, default=card_options)
selected_channels = st.sidebar.multiselect("Sales Channel", channel_options, default=channel_options)

filtered = df[
    (df["date"] == selected_date) &
    (df["card_brand"].isin(selected_cards)) &
    (df["channel"].isin(selected_channels))
]

# === KPI Summary ===
st.subheader(f"📌 Summary for {selected_date}")
k1, k2, k3 = st.columns(3)

k1.metric("Total Orders", len(filtered))
k2.metric("Total Revenue", f"${filtered['gross_sales'].sum():,.2f}")
k3.metric(
    "Avg Order Value",
    f"${filtered['gross_sales'].mean():.2f}" if not filtered.empty else "$0.00"
)

st.markdown("---")

# === Hourly Revenue Heatmap ===
st.subheader("🕒 Hourly Revenue Heatmap (All Dates)")
heat_df = df.groupby(["weekday", "hour"])["gross_sales"].sum().reset_index()

heat = alt.Chart(heat_df).mark_rect().encode(
    x=alt.X("hour:O", title="Hour of Day"),
    y=alt.Y("weekday:N", sort=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]),
    color=alt.Color("gross_sales:Q", scale=alt.Scale(scheme="blues"), title="Revenue ($)"),
    tooltip=["weekday:N", "hour:O", "gross_sales:Q"]
).properties(height=420)

st.altair_chart(heat, use_container_width=True)
st.markdown("> 💡 Use this view to optimize hourly staffing and promo timing based on weekday heat zones.")

# === Top Items Table ===
st.subheader("🏆 Top Items Sold on Selected Day")
top_items = (
    filtered.groupby("item")["gross_sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
    .head(15)
)

if not top_items.empty:
    st.dataframe(top_items, use_container_width=True)
else:
    st.info("No item data available for the selected filters.")

# === Bonus Insights ===
st.markdown("---")

st.subheader("📅 Total Revenue by Weekday")
weekday_df = fetch_query("sql/revenue_by_weekday.sql")
if not weekday_df.empty:
    weekday_chart = px.bar(weekday_df, x="weekday", y="total_revenue", title=None, labels={"total_revenue": "Revenue ($)"})
    weekday_chart.update_layout(height=360)
    st.plotly_chart(weekday_chart, use_container_width=True)
    st.markdown("> 🔄 Identify which days consistently drive the most revenue and plan inventory accordingly.")
else:
    st.info("No weekday revenue data available.")

st.subheader("⏱️ Peak Ordering Hours")
peak_df = fetch_query("sql/peak_hours.sql")
if not peak_df.empty:
    st.dataframe(peak_df, use_container_width=True)
else:
    st.info("No peak hour data available.")

st.subheader("🧃 Bundle Effect Insights")
bundle_df = fetch_query("sql/bundle_effect.sql")
if not bundle_df.empty:
    st.dataframe(bundle_df, use_container_width=True)
else:
    st.info("No bundle effect data available.")

# === Footer ===
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Use this dashboard to fine-tune prep, shifts, and product pairings.</div>",
    unsafe_allow_html=True
)
