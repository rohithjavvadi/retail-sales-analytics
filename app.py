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
# REVENUE BY STATE
# ==========================================================

state_sales = (
    df.groupby("CUSTOMER_STATE")["PRICE"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

state_chart = px.bar(
    state_sales,
    x="CUSTOMER_STATE",
    y="PRICE",
    title="Revenue by Customer State"
)

state_chart.update_layout(
    xaxis_title="State",
    yaxis_title="Revenue ($)"
)

# ==========================================================
# TOP SELLERS
# ==========================================================

seller_sales = (
    df.groupby("SELLER_ID")["PRICE"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

seller_chart = px.bar(
    seller_sales,
    x="PRICE",
    y="SELLER_ID",
    orientation="h",
    title="Top 10 Sellers"
)

seller_chart.update_layout(
    xaxis_title="Revenue ($)",
    yaxis_title=""
)

# ==========================================================
# DASHBOARD ROW 2
# ==========================================================

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(
        state_chart,
        use_container_width=True
    )

with col4:
    st.plotly_chart(
        seller_chart,
        use_container_width=True
    )

# ==========================================================
# SALES DATA
# ==========================================================

st.subheader("Sales Data")

st.dataframe(
    df,
    use_container_width=True
)
# ==========================================================
# DOWNLOAD DATA
# ==========================================================

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Data as CSV",
    data=csv,
    file_name="retailiq_sales.csv",
    mime="text/csv"
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

