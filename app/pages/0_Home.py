# 0_Home.py – Welcome Landing Page for Toasted Bean Dashboard

import streamlit as st
from datetime import date

# === Page Setup ===
st.set_page_config(page_title="Toasted Bean Dashboard", layout="centered")

# === Branding ===
st.title("☕ Toasted Bean Coffee Truck")
st.subheader("Interactive Sales Dashboard")

# === Introduction ===
st.markdown("""
Welcome to your personalized dashboard for Toasted Bean Coffee Truck — built to turn Square POS data into real-time, actionable business insights.

Use the sidebar to explore:
- **📈 Weekly Overview** – Track KPIs, revenue, and item performance week over week.
- **💡 Top Items** – Explore top-selling products by category and sales channel.
- **📊 Category Trends** – View monthly shifts in product categories to guide planning.
- **📅 Daily Insights** – Optimize daily prep, staffing, and inventory timing.
""")

# === Business Snapshot Block ===
st.markdown("---")
st.subheader("📌 Current Data Status")
st.info("This dashboard reflects data through: **{}**".format(date.today().strftime("%B %d, %Y")))

# === Footer ===
st.markdown("---")
st.markdown("<div style='text-align:center; color:gray;'>Built by Ken Valenzuela · MS-AIB Candidate · Powered by Streamlit + PostgreSQL</div>", unsafe_allow_html=True)
