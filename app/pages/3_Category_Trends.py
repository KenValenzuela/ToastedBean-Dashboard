# app/pages/3_Category_Trends.py

import streamlit as st
import pandas as pd
import altair as alt
from utils import fetch_query

st.title("📊 Category Sales Trends")
st.caption("Analyze category-level revenue trends across date ranges.")

# === Load Data ===
df = fetch_query("sql/revenue_by_category.sql")

if df.empty:
    st.warning("No data available.")
    st.stop()

# === Drop nulls if any ===
df = df.dropna(subset=["date_range", "category", "total_revenue"])

# === Filter Sidebar ===
ranges = df["date_range"].unique().tolist()
selected_ranges = st.multiselect("Select Date Range(s):", ranges, default=ranges)
filtered_df = df[df["date_range"].isin(selected_ranges)]

# === Chart ===
if not filtered_df.empty:
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("total_revenue:Q", title="Total Revenue ($)"),
        y=alt.Y("category:N", sort='-x'),
        color=alt.Color("category:N", legend=None),
        tooltip=["category", "total_revenue", "date_range"]
    ).properties(height=400, width=700)

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No data available for selected range(s).")
