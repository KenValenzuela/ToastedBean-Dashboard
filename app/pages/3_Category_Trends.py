# app/pages/3_Category_Trends.py

import streamlit as st
import pandas as pd
import altair as alt
from utils import fetch_query

st.title("📊 Category Sales Trends")
st.caption("Analyze category-level revenue trends by month.")

# === Load Data ===
df = fetch_query("sql/revenue_by_category.sql")

if df.empty or "start_date" not in df.columns:
    st.warning("No data available.")
    st.stop()

# === Parse and Clean ===
df["month"] = pd.to_datetime(df["start_date"], errors="coerce").dt.to_period("M").dt.to_timestamp()
df = df.dropna(subset=["month", "category", "revenue"])
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")

# === Filter Sidebar ===
months = df["month"].dt.strftime("%B %Y").sort_values().unique().tolist()
selected = st.multiselect("Select Month(s):", months, default=months)
filtered_df = df[df["month"].dt.strftime("%B %Y").isin(selected)]

# === Chart ===
if not filtered_df.empty:
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("revenue:Q", title="Total Revenue ($)"),
        y=alt.Y("category:N", sort='-x'),
        color=alt.Color("category:N", legend=None),
        tooltip=["category", "revenue", "month"]
    ).properties(height=400, width=700)

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No data available for selected month(s).")
