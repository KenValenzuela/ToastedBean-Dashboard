# app/main.py

import streamlit as st
from utils import fetch_query
import pandas as pd
import plotly.express as px
from datetime import datetime

# === Config ===
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

# === Helper: Anonymize Names ===
def anonymize_customer_names(df, column="customer_name"):
    if column in df.columns:
        unique_names = df[column].dropna().unique()
        name_map = {name: f"Customer_{i+1:03d}" for i, name in enumerate(unique_names)}
        df[column] = df[column].map(name_map)
    return df

# === Load Queries ===
revenue_df   = fetch_query("sql/sales_trends.sql")
aov_df       = fetch_query("sql/avg_items_per_order.sql")
payment_df   = fetch_query("sql/aov_by_payment_method.sql")
category_df  = fetch_query("sql/revenue_by_category.sql")
loyalty_df   = fetch_query("sql/top_returning_customers.sql")
alert_df     = fetch_query("sql/low_traffic_alerts.sql")

# === Normalize revenue_df ===
if revenue_df.empty or "date_range" not in revenue_df.columns:
    st.error("🚨 Could not load revenue data. Ensure `sales_trends.sql` returns `date_range` and `total_amount`.")
    st.stop()

revenue_df = revenue_df.rename(columns={
    "date_range": "date",
    "total_amount": "gross_sales"
})
revenue_df["date"] = revenue_df["date"].str.extract(r"(\d{2}/\d{2}/\d{4})")[0]
revenue_df["date"] = pd.to_datetime(revenue_df["date"], format="%m/%d/%Y", errors="coerce")

# === MTD Filter ===
today = pd.to_datetime(datetime.now().date())
start_month = today.replace(day=1)
mtd_df = revenue_df[revenue_df["date"] >= start_month].copy()

# === Loyalty table processing ===
loyalty_df = anonymize_customer_names(loyalty_df, column="customer_name")
if "customer_id" in loyalty_df.columns:
    loyalty_df.drop(columns=["customer_id"], inplace=True)

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
    fig = px.line(mtd_df, x="date", y="gross_sales", markers=True)
    fig.update_layout(height=380, xaxis_title="Date", yaxis_title="Gross Sales ($)", showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
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

# === Footer ===
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: gray;'>Last updated: {today.strftime('%B %d, %Y')}</div>", unsafe_allow_html=True)

