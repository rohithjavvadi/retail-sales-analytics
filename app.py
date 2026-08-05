import pandas as pd
import streamlit as st
import snowflake.connector  as snowflake
import plotly.express as px

from snowflake_connection import run_query

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="RetailIQ Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 RetailIQ Executive Dashboard")
st.markdown("### Snowflake Data Warehouse Dashboard")

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    query = """
    SELECT *
    FROM VW_MASTER_SALES
    """
    return run_query(query)

df = load_data()
# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_revenue = df["PRICE"].sum()

total_orders = df["ORDER_ID"].nunique()

total_customers = df["CUSTOMER_ID"].nunique()

avg_order_value = total_revenue / total_orders

# ==========================================================
# KPI CARDS
# ==========================================================

st.subheader("📈 Executive KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Revenue",
        f"${total_revenue:,.2f}"
    )

with col2:
    st.metric(
        "📦 Orders",
        f"{total_orders:,}"
    )

with col3:
    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

with col4:
    st.metric(
        "🛒 Avg Order Value",
        f"${avg_order_value:,.2f}"
    )

st.divider()

# ==========================================================
# SHOW DATA
# ==========================================================

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_revenue = df["PRICE"].sum()

total_orders = df["ORDER_ID"].nunique()

total_customers = df["CUSTOMER_ID"].nunique()

avg_order_value = total_revenue / total_orders

# ==========================================================
# KPI CARDS
# ==========================================================

st.subheader("📈 Executive KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "💰 Revenue",
        f"${total_revenue:,.2f}"
    )

with col2:
    st.metric(
        "📦 Orders",
        f"{total_orders:,}"
    )

with col3:
    st.metric(
        "👥 Customers",
        f"{total_customers:,}"
    )

with col4:
    st.metric(
        "🛒 Avg Order Value",
        f"${avg_order_value:,.2f}"
    )

st.divider()

# ==========================================================
# MONTHLY REVENUE
# ==========================================================

monthly_sales = (
    df.groupby("PURCHASE_MONTH")["PRICE"]
    .sum()
    .reset_index()
    .sort_values("PURCHASE_MONTH")
)

monthly_chart = px.line(
    monthly_sales,
    x="PURCHASE_MONTH",
    y="PRICE",
    markers=True,
    title="Monthly Revenue Trend"
)

monthly_chart.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue ($)"
)

# ==========================================================
# TOP PRODUCT CATEGORIES
# ==========================================================

category_sales = (
    df.groupby("PRODUCT_CATEGORY_NAME_ENGLISH")["PRICE"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

category_chart = px.bar(
    category_sales,
    x="PRICE",
    y="PRODUCT_CATEGORY_NAME_ENGLISH",
    orientation="h",
    title="Top 10 Product Categories"
)

category_chart.update_layout(
    xaxis_title="Revenue ($)",
    yaxis_title=""
)

# ==========================================================
# DASHBOARD ROW 1
# ==========================================================

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(
        monthly_chart,
        use_container_width=True
    )

with col2:
    st.plotly_chart(
        category_chart,
        use_container_width=True
    )

