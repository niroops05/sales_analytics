import streamlit as st
import pandas as pd
from datetime import datetime

from database.mongo_client import insert_sale, fetch_all_sales
from logic.kpi_calculations import (
    prepare_month_column,
    calculate_kpis,
    monthly_trend,
    product_performance,
    region_performance
)
from visuals.charts import line_chart, bar_chart

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")

st.title("📊 Sales Performance Dashboard (Real-Time)")
st.markdown("Designed for **management-level decision making** using MongoDB Atlas.")

# ---------------- LOAD DATA FROM MONGODB ----------------
df = fetch_all_sales()

# Handle empty DB safely
if df.empty:
    st.info("No sales data yet. Add records to begin.")

# ---------------- SAFE DYNAMIC OPTIONS ----------------
if df.empty:
    product_options = ["Product A"]
    region_options = ["North"]
else:
    product_options = sorted(df["Product"].dropna().unique().tolist())
    region_options = sorted(df["Region"].dropna().unique().tolist())

# ---------------- SIDEBAR: REAL-TIME INPUT ----------------
st.sidebar.header("➕ Add New Sale")

date = st.sidebar.date_input("Date", datetime.today())
region = st.sidebar.selectbox("Region", region_options)
product = st.sidebar.selectbox("Product", product_options)
units = st.sidebar.number_input("Units Sold", min_value=1, value=1)
price = st.sidebar.number_input("Revenue per Unit (₹)", min_value=0.0, value=100.0)

if st.sidebar.button("Add Sale"):
    new_sale = {
        "Date": date,
        "Region": region,
        "Product": product,
        "Units Sold": int(units),
        "Revenue": float(units * price)
    }

    insert_sale(new_sale)
    st.sidebar.success("✅ Sale saved to MongoDB Atlas!")

    # Reload data after insert
    df = fetch_all_sales()

# ---------------- KPI SECTION ----------------
if not df.empty:
    df = prepare_month_column(df)

    total_revenue, best_product, best_region = calculate_kpis(df)

    st.subheader("📌 Key Performance Indicators")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
    c2.metric("Best Product", best_product)
    c3.metric("Top Region", best_region)

    st.divider()

    # ---------------- VISUALIZATIONS ----------------
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            line_chart(
                monthly_trend(df),
                "Month",
                "Revenue",
                "📈 Monthly Revenue Trend"
            ),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            bar_chart(
                product_performance(df),
                "Product",
                "Revenue",
                "📦 Product Performance"
            ),
            use_container_width=True
        )

    st.plotly_chart(
        bar_chart(
            region_performance(df),
            "Region",
            "Revenue",
            "🌍 Region-wise Performance"
        ),
        use_container_width=True
    )

    st.divider()

    # ---------------- RAW DATA ----------------
    st.subheader("📄 Live Sales Data (MongoDB Atlas)")
    st.dataframe(df, use_container_width=True)
