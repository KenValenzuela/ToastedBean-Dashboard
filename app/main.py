# app/main.py

import streamlit as st
from utils import fetch_query
import pandas as pd
import plotly.express as px
from datetime import datetime

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

# === Column Normalization ===
if "date_range" in revenue_df.columns:
    revenue_df.rename(columns={"date_range": "date"}, inplace=True)
if "total_amount" in revenue_df.columns:
    revenue_df.rename(columns={"total_amount": "gross_sales"}, inplace=True)
if "date_range" in category_df.columns:
    category_df.rename(columns={"date_range": "month"}, inplace=True)

# === Convert Dates ===
if revenue_df["date"].dtype == object:
    revenue_df["date"] = revenue_df["date"].str.extract(r"(\d{2}/\d{2}/\d{4})")[0]
revenue_df["date"] = pd.to_datetime(revenue_df["date"], format="%m/%d/%Y", errors="coerce")

# === Month-to-Date Filter ===
today = pd.to_datetime(datetime.now().date())
start_month = today.replace(day=1)
mtd_df = revenue_df[revenue_df["date"] >= start_month].copy()

# === KPIs ===
st.subheader("Key Metrics — Month to Date")
k1, k2, k3 = st.columns(3)
k1.metric("Total Gross Sales", f"${mtd_df['gross_sales'].sum():,.2f}")
k2.metric("Avg Order Value", f"${aov_df.get('avg_order_value', [None])[0]:,.2f}" if not aov_df.empty else "N/A")
k3.metric("Avg Items per Order", f"{aov_df.get('avg_items_per_order', [None])[0]:.2f}" if not aov_df.empty else "N/A")
st.markdown("---")

# === Revenue Trend ===
st.subheader("Revenue Trend (Daily)")
if not mtd_df.empty:
    line_fig = px.line(mtd_df, x="date", y="gross_sales", markers=True)
    line_fig.update_layout(height=380, xaxis_title="Date", yaxis_title="Gross Sales ($)", showlegend=False)
    st.plotly_chart(line_fig, use_container_width=True)
else:
    st.info("No revenue data available for the current month.")

# === Payment Mix ===
st.subheader("Payment Method Mix")
if not payment_df.empty:
    fig = px.bar(payment_df, x="total_orders", y="payment_method", orientation="h", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No payment data available.")

# === Category Sales ===
st.subheader("Top Revenue Categories (MTD)")
if not category_df.empty:
    fig = px.bar(category_df, x="total_revenue", y="category", orientation="h", text_auto=True)
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No category sales data available.")

# === Loyalty Table ===
st.subheader("Top Returning Customers")
if not loyalty_df.empty:
    st.dataframe(loyalty_df.head(10), use_container_width=True)
else:
    st.info("No returning customer data found.")

# === Traffic Alerts ===
st.subheader("Traffic Insights (Last 30 Days)")
if not alert_df.empty and "traffic_flag" in alert_df.columns:
    st.dataframe(alert_df[["date", "orders", "traffic_flag"]], use_container_width=True)
else:
    st.info("No traffic insights available.")

st.markdown("---")
st.markdown(f"<div style='text-align: center; color: gray;'>Last updated: {today.strftime('%B %d, %Y')}</div>", unsafe_allow_html=True)
