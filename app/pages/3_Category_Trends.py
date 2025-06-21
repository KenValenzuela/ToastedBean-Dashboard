# app/pages/3_Category_Trends.py

import streamlit as st
import pandas as pd
import altair as alt
from utils import fetch_query

st.title("📊 Category Sales Trends")
st.caption("Analyze category-level revenue trends by month.")

# === Load Data ===
df = fetch_query("sql/revenue_by_category.sql")

if df.empty:
    st.warning("No data available.")
    st.stop()

# === Parse and Clean ===
df["month"] = pd.to_datetime(df["month"], errors="coerce")
df = df.dropna(subset=["month", "category", "total_revenue"])

# === Filter Sidebar ===
months = df["month"].dt.strftime("%B %Y").unique().tolist()
selected = st.multiselect("Select Month(s):", months, default=months)
filtered_df = df[df["month"].dt.strftime("%B %Y").isin(selected)]

# === Chart ===
if not filtered_df.empty:
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("total_revenue:Q", title="Total Revenue ($)"),
        y=alt.Y("category:N", sort='-x'),
        color=alt.Color("category:N", legend=None),
        tooltip=["category", "total_revenue", "month"]
    ).properties(height=400, width=700)

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No data available for selected month(s).")
