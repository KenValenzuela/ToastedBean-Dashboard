# ☕ Toasted Bean Coffee Truck Dashboard

This project started as a favor for a friend — the co-owner of a mobile coffee truck in Arizona. What began as a quick ask to “make sense of our sales” evolved into a complete analytics dashboard that now powers their weekly business decisions.

---

## 📊 Overview

Toasted Bean is a small, independently-owned coffee truck that uses Square POS for transactions — but like many small businesses, they relied entirely on exported spreadsheets to manage inventory, understand sales trends, and plan ahead.

I partnered with the team to replace manual review processes with a clean, interactive Streamlit dashboard that helps them answer:

- What are our top-selling items and categories?
- Which days underperform, and how should we adjust?
- Are modifiers (like extra espresso or alt milk) actually increasing order value?
- Are customers returning — and how much are they spending?

---

## 🧠 Key Features

The dashboard is built using **Streamlit**, **PostgreSQL**, and **Python**, and includes:

### 1. Executive Summary
- Month-to-date revenue, AOV, item count per order
- Daily revenue trend line
- Payment method and tip breakdown

### 2. Top-Selling Items
- Filterable by month, sales channel, and product category
- Interactive bar charts showing revenue leaders

### 3. Category Trends
- Line charts comparing category-level momentum
- Multi-month performance views with filters

### 4. Daily Insights
- Weekday breakdowns with low-traffic alerts
- Modifier effectiveness scoring

### 5. Loyalty Tracking
- Identifies top returning customers by order count and spend

---

## 🛠️ How It Works

1. **Data Cleaning**  
   Square CSV exports are cleaned using `pandas` and prepped for analysis.

2. **Data Loading**  
   Cleaned data is inserted into a normalized **PostgreSQL schema** using SQLAlchemy.

3. **Query Layer**  
   Business logic lives in modular `.sql` files for reuse and testability.

4. **App Interface**  
   A four-page **Streamlit** dashboard presents KPIs, charts, and filters for decision-making.

---

## ⚙️ Tech Stack

| Layer              | Tools Used                            |
|-------------------|----------------------------------------|
| Front-End          | Streamlit (with branding + filters)    |
| Back-End Querying  | PostgreSQL + modular SQL queries       |
| Data Processing    | Python (pandas, SQLAlchemy, dotenv)    |
| Visualization      | Plotly + Altair                        |

---

## 🚀 Business Impact

Since launching, the dashboard has helped Toasted Bean:

- Promote their most profitable items
- Adjust staffing on slow weekdays
- Understand how card vs. cash affects tips and fees
- Quantify the revenue impact of common modifiers
- Begin identifying and tracking repeat customer behavior

It’s a real-world example of what happens when data is made usable — turning CSVs into tools that drive decisions.

---

## 🔧 Status

✅ Actively maintained  
🛠️ Upcoming enhancements:
- Inventory tracking integration
- Shift-based performance breakdowns
- Google Sheets sync for daily reporting

---

## 👋 About the Creator

**Ken Valenzuela**  
ASU MS-AIB Candidate | Data Scientist & Business Analyst  
> Helping small businesses think like big ones — with data.

- [GitHub](https://github.com/KenValenzuela)  
- [LinkedIn](https://www.linkedin.com/in/ken-valenzuela)

