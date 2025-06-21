# app/pages/1_Overview.py

import streamlit as st
from utils import fetch_query
import pandas as pd
import plotly.express as px
from datetime import timedelta

# === Setup ===
st.set_page_config(page_title="Weekly Business Overview", layout="wide")
st.title("📈 Weekly Performance Snapshot")
st.caption("Review key business metrics across sales, order volume, and product performance.")
st.markdown("---")

# === Load Data ===
df = fetch_query("sql/detail_items.sql")
df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce", utc=True)
df = df.dropna(subset=["datetime"])
df["date"] = df["datetime"].dt.normalize()

if df.empty or df["date"].isna().all():
    st.error("No usable datetime data returned from SQL query.")
    st.stop()

latest_day = df["date"].max()
if pd.isnull(latest_day):
    st.warning("No valid recent data found.")
    st.stop()

st.markdown(f"📅 **Date Range:** {df['date'].min().strftime('%b %d')} – {latest_day.strftime('%b %d, %Y')}")

week_start = latest_day - timedelta(days=6)
prev_week_start = week_start - timedelta(days=7)
prev_week_end = week_start - timedelta(days=1)

this_week = df[(df["date"] >= week_start) & (df["date"] <= latest_day)]
last_week = df[(df["date"] >= prev_week_start) & (df["date"] <= prev_week_end)]

# === KPIs ===
st.subheader("📊 Week-over-Week KPIs")
k1, k2, k3 = st.columns(3)

this_revenue = this_week["gross_sales"].sum()
last_revenue = last_week["gross_sales"].sum()
wow_delta = ((this_revenue - last_revenue) / last_revenue) if last_revenue != 0 else 0

k1.metric("Revenue This Week", f"${this_revenue:,.2f}")
k2.metric("Orders This Week", len(this_week))
k3.metric("Revenue Change", f"{wow_delta:.1%}", delta_color="inverse")

st.markdown("> 📌 Revenue is {} compared to last week.{}".format(
    "up" if wow_delta > 0 else "down",
    f" Notable lift in sales from {week_start.strftime('%A')} to {latest_day.strftime('%A')}."
))

st.markdown("---")

# === Daily Revenue Trend ===
st.subheader("📅 Daily Revenue – Last 14 Days")
trend_df = df[df["date"] >= prev_week_start]
daily = trend_df.groupby("date")["gross_sales"].sum().reset_index()

if not daily.empty:
    fig = px.bar(
        daily,
        x="date",
        y="gross_sales",
        labels={"gross_sales": "Revenue ($)", "date": "Date"},
    )
    fig.update_layout(height=360)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No revenue data available for this period.")

# === Top Items This Week ===
st.subheader("🏆 Top 10 Items This Week")
top_items = (
    this_week.groupby("item")["gross_sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

if not top_items.empty:
    item_fig = px.bar(
        top_items,
        x="gross_sales",
        y="item",
        orientation="h",
        text_auto=".2s",
        labels={"gross_sales": "Revenue ($)", "item": "Item"},
    )
    item_fig.update_layout(height=400, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(item_fig, use_container_width=True)
else:
    st.info("No item-level revenue available this week.")

# === Modifier Insights ===
st.subheader("✨ Top Modifiers by Revenue Impact")
mod_df = fetch_query("sql/modifier_lift.sql")

if not mod_df.empty:
    st.dataframe(mod_df.head(10), use_container_width=True)
else:
    st.info("No modifier data available for the current week.")

# === Footer ===
st.markdown("---")
st.markdown(
    f"<div style='text-align: center; color: gray;'>Report updated through {latest_day.strftime('%B %d, %Y')}</div>",
    unsafe_allow_html=True
)