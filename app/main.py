# app/main.py

import streamlit as st
from utils import fetch_query
import pandas as pd
import plotly.express as px
from datetime import datetime

# === Page Setup ===
st.set_page_config(
    page_title="Toasted Bean Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.image("assets/toastedbean.png", use_column_width=False, width=180)

st.title("Toasted Bean Coffee Truck – Executive Summary")
st.caption("Month-to-date performance overview across revenue, order behavior, and traffic signals.")
st.markdown("---")

# === Load Queries ===
revenue_df = fetch_query("sql/sales_trends.sql")
aov_df = fetch_query("sql/avg_items_per_order.sql")
payment_df = fetch_query("sql/aov_by_payment_method.sql")
category_df = fetch_query("sql/revenue_by_category.sql")
loyalty_df = fetch_query("sql/top_returning_customers.sql")
alert_df = fetch_query("sql/low_traffic_alerts.sql")

# === Standardize Column Names ===
if "date" not in revenue_df.columns and "date_range" in revenue_df.columns:
    revenue_df.rename(columns={"date_range": "date"}, inplace=True)
if "gross_sales" not in revenue_df.columns and "total_amount" in revenue_df.columns:
    revenue_df.rename(columns={"total_amount": "gross_sales"}, inplace=True)
if "date_range" in category_df.columns:
    category_df.rename(columns={"date_range": "month"}, inplace=True)

# === Extract Start Date from Range for MTD Filter ===
if revenue_df["date"].dtype == object:
    revenue_df["date"] = revenue_df["date"].str.extract(r"(\d{2}/\d{2}/\d{4})")[0]
revenue_df["date"] = pd.to_datetime(revenue_df["date"], format="%m/%d/%Y", errors="coerce")

# === MTD Filtering ===
today = pd.to_datetime(datetime.now().date())
start_month = today.replace(day=1)
mtd_df = revenue_df[revenue_df["date"] >= start_month].copy()

# === KPIs ===
st.subheader("Key Metrics — Month to Date")
k1, k2, k3 = st.columns(3)

k1.metric("Total Gross Sales", f"${mtd_df['gross_sales'].sum():,.2f}")

if not aov_df.empty and pd.notnull(aov_df['avg_order_value'].iloc[0]):
    k2.metric("Avg Order Value", f"${aov_df['avg_order_value'].iloc[0]:,.2f}")
else:
    k2.metric("Avg Order Value", "N/A")

if not aov_df.empty and pd.notnull(aov_df['avg_items_per_order'].iloc[0]):
    k3.metric("Avg Items per Order", f"{aov_df['avg_items_per_order'].iloc[0]:.2f}")
else:
    k3.metric("Avg Items per Order", "N/A")

st.markdown("---")

# === Revenue Trend Chart ===
st.subheader("Revenue Trend (Daily)")
if not mtd_df.empty:
    line_fig = px.line(
        mtd_df,
        x="date",
        y="gross_sales",
        markers=True,
        labels={"date": "Date", "gross_sales": "Gross Sales"},
    )
    line_fig.update_traces(line=dict(width=3))
    line_fig.update_layout(height=380, xaxis_title="Date", yaxis_title="Gross Sales ($)", showlegend=False)
    st.plotly_chart(line_fig, use_container_width=True)
else:
    st.info("No revenue data available for the current month.")

# === Payment Mix ===
st.subheader("Payment Method Mix")
if not payment_df.empty:
    payment_bar = px.bar(
        payment_df.sort_values("total_orders", ascending=True),
        x="total_orders",
        y="payment_method",
        orientation="h",
        text_auto=True,
        labels={"payment_method": "Payment Method", "total_orders": "Order Count"},
    )
    payment_bar.update_layout(height=320, yaxis_title=None, xaxis_title="Orders")
    st.plotly_chart(payment_bar, use_container_width=True)
else:
    st.info("No payment method data available.")

# === Category Revenue ===
st.subheader("Top Revenue Categories (MTD)")
if not category_df.empty:
    category_bar = px.bar(
        category_df.sort_values("total_revenue", ascending=True),
        x="total_revenue",
        y="category",
        orientation="h",
        text_auto=True,
        labels={"category": "Category", "total_revenue": "Revenue"},
    )
    category_bar.update_layout(height=400, yaxis_title=None, xaxis_title="Total Revenue ($)")
    st.plotly_chart(category_bar, use_container_width=True)
else:
    st.info("No category sales data available.")

# === Top Returning Customers ===
st.subheader("Top Returning Customers")
if not loyalty_df.empty:
    loyalty_subset = loyalty_df[["customer_name", "total_visits", "total_spent"]].head(10)
    st.dataframe(loyalty_subset, use_container_width=True)
else:
    st.info("No returning customer data found.")

# === Traffic Alerts ===
st.subheader("Traffic Insights (Last 30 Days)")
if not alert_df.empty and "traffic_flag" in alert_df.columns:
    low_days = alert_df[alert_df["traffic_flag"].str.contains("BELOW", na=False)]
    high_days = alert_df[alert_df["traffic_flag"].str.contains("ABOVE", na=False)]

    if not low_days.empty:
        st.warning("📉 Below-average order volume:")
        st.dataframe(low_days[["date", "orders", "total_sales", "traffic_flag"]], use_container_width=True)
    else:
        st.success("✅ No below-average days.")

    if not high_days.empty:
        st.success("📈 Above-average order volume:")
        st.dataframe(high_days[["date", "orders", "total_sales", "traffic_flag"]], use_container_width=True)
    else:
        st.info("No above-average traffic spikes detected.")
else:
    st.info("No traffic data available.")

# === Footer ===
st.markdown("---")
if pd.notnull(today):
    st.markdown(
        f"<div style='text-align: center; color: gray;'>Last updated: {today.strftime('%B %d, %Y')}</div>",
        unsafe_allow_html=True
    )
