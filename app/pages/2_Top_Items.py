# app/pages/2_Top_Items.py

import streamlit as st
from utils import fetch_query
import pandas as pd
import plotly.express as px

# === Page Setup ===
st.set_page_config(page_title="Top Items", layout="wide")
st.title("🏅 Top-Selling Items")
st.caption("Explore top-performing products by revenue. Filter by month, channel, and category to uncover sales drivers.")
st.markdown("---")

# === Load Data ===
df = fetch_query("sql/detail_items.sql")
df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce", utc=True)
df = df.dropna(subset=["datetime"])
df["date"] = df["datetime"].dt.date
df["month"] = pd.to_datetime(df["datetime"].astype(str), errors="coerce").dt.to_period("M").astype(str)

# === Ensure Valid Columns Exist ===
required_cols = ["gross_sales", "channel", "category", "item", "month"]
if df.empty or not all(col in df.columns for col in required_cols):
    st.warning("No valid item sales data available.")
    st.stop()

# === Sidebar Filters ===
st.sidebar.header("📂 Filter Options")
month_options = sorted(df["month"].dropna().unique(), reverse=True)
channel_options = sorted(df["channel"].dropna().unique())
category_options = sorted(df["category"].dropna().unique())

if not month_options:
    st.warning("No monthly data available.")
    st.stop()

selected_month = st.sidebar.selectbox("Select Month", month_options)
selected_channel = st.sidebar.multiselect("Sales Channel", channel_options, default=channel_options)
selected_category = st.sidebar.multiselect("Category", category_options, default=category_options)

# === Apply Filters ===
filtered = df[
    (df["month"] == selected_month) &
    (df["channel"].isin(selected_channel)) &
    (df["category"].isin(selected_category))
]

# === Top Items Chart ===
st.subheader(f"📌 Top 15 Items – {selected_month}")

if not filtered.empty:
    top_items = (
        filtered.groupby("item")["gross_sales"]
        .sum()
        .sort_values(ascending=False)
        .head(15)
        .reset_index()
    )

    top_fig = px.bar(
        top_items,
        x="gross_sales",
        y="item",
        orientation="h",
        text_auto=".2s",
        labels={"gross_sales": "Revenue ($)", "item": "Item"},
    )
    top_fig.update_layout(
        height=450,
        yaxis={"categoryorder": "total ascending"},
        xaxis_title="Gross Sales ($)",
        yaxis_title=None,
        showlegend=False
    )
    st.plotly_chart(top_fig, use_container_width=True)

    st.markdown(f"> 📈 These items drove the most revenue in {selected_month}. Use category/channel filters to refine your view.")
else:
    st.info("No item-level sales found for the selected filters.")

# === Modifier Lift Section ===
st.subheader("✨ Top Modifiers by Revenue Lift")
mod_df = fetch_query("sql/modifier_lift.sql")

if not mod_df.empty:
    st.dataframe(mod_df.head(15), use_container_width=True)
else:
    st.info("No modifier lift data available.")

# === Footer ===
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>Use filters to explore revenue drivers by item and modifier.</div>",
    unsafe_allow_html=True
)
