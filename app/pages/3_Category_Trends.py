# app/pages/3_Category_Trends.py

import streamlit as st
import pandas as pd
import altair as alt
from utils import fetch_query

# === Page Setup ===
st.set_page_config(page_title="Category Trends", layout="wide")
st.title("Category Revenue Trends")
st.caption("Visualize monthly trends across product categories to spot momentum or decline.")
st.markdown("---")

# === Load & Prepare Data ===
df = fetch_query("sql/revenue_by_category.sql")

# Rename 'date_range' to 'month' if needed
if "month" not in df.columns and "date_range" in df.columns:
    df.rename(columns={"date_range": "month"}, inplace=True)

# Show raw for debugging
st.write("🧪 Raw category data sample:")
st.dataframe(df.head(10))

# Attempt to extract the first date from a range like "05/01/2025–05/31/2025"
df["month"] = df["month"].str.extract(r"(\d{2}/\d{2}/\d{4})")
df["month"] = pd.to_datetime(df["month"], errors="coerce")
df = df.dropna(subset=["month", "category", "total_revenue"])

if df.empty:
    st.warning("No valid category trend data available.")
    st.stop()

# Derive 'month_str' for grouping
df["month_str"] = df["month"].dt.to_period("M").astype(str)

# === Sidebar Filters ===
st.sidebar.header("Filter Options")

unique_months = sorted(df["month_str"].unique(), reverse=True)
unique_categories = sorted(df["category"].dropna().unique())

selected_months = st.sidebar.multiselect(
    "Select Months",
    options=unique_months,
    default=unique_months[:3] if unique_months else []
)

selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=unique_categories,
    default=list(unique_categories)
)

# === Filter Data ===
filtered_df = df[
    (df["month_str"].isin(selected_months)) &
    (df["category"].isin(selected_categories))
]

# === Revenue Trend Chart ===
st.subheader("Revenue Trend by Category")

if not filtered_df.empty:
    trend_chart = alt.Chart(filtered_df).mark_line(point=True).encode(
        x=alt.X("month:T", title="Month"),
        y=alt.Y("total_revenue:Q", title="Revenue ($)", stack=None),
        color=alt.Color("category:N", title="Category"),
        tooltip=["month:T", "category:N", "total_revenue:Q"]
    ).properties(
        height=420
    ).interactive()

    st.altair_chart(trend_chart, use_container_width=True)
else:
    st.info("No data available for the selected filters.")

# === Summary Table ===
st.subheader("Total Revenue by Category (Filtered Period)")

summary_df = (
    filtered_df
    .groupby("category")["total_revenue"]
    .sum()
    .reset_index()
    .sort_values("total_revenue", ascending=False)
)

if not summary_df.empty:
    st.dataframe(summary_df, use_container_width=True)
else:
    st.warning("No category summary available.")

# === Footer ===
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Use filters to explore category performance over time.</div>",
    unsafe_allow_html=True
)
