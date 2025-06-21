# app/pages/3_Category_Trends.py

import streamlit as st
import pandas as pd
import altair as alt
from utils import fetch_query

st.title("📊 Category Sales Trends")
st.caption("Analyze category-level revenue trends across months.")

# === Load Data ===
df = fetch_query("sql/revenue_by_category.sql")

if df.empty:
    st.warning("No data available.")
    st.stop()

# === Convert Month Column to datetime if needed ===
if not pd.api.types.is_datetime64_any_dtype(df["month"]):
    df["month"] = pd.to_datetime(df["month"], errors="coerce")

# === Drop any nulls after parsing ===
df = df.dropna(subset=["month", "category", "total_revenue"])

# === Filter Sidebar ===
months = df["month"].dt.strftime("%B %Y").unique()
selected_months = st.multiselect("Select Month(s):", months, default=months)
filtered_df = df[df["month"].dt.strftime("%B %Y").isin(selected_months)]

# === Chart ===
if not filtered_df.empty:
    chart = alt.Chart(filtered_df).mark_bar().encode(
        x=alt.X("total_revenue:Q", title="Total Revenue ($)"),
        y=alt.Y("category:N", sort='-x'),
        color=alt.Color("category:N", legend=None),
        tooltip=["category", "total_revenue"]
    ).properties(height=400, width=700)

    st.altair_chart(chart, use_container_width=True)
else:
    st.info("No data available for selected month(s).")
