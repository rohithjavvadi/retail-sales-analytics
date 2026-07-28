from pathlib import Path
import sqlite3

import pandas as pd
import plotly.express as px
import streamlit as st

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="RetailIQ Executive Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 RetailIQ Executive Dashboard")
st.markdown("### Interactive Business Intelligence Dashboard")

# ==========================================================
# DATABASE CONNECTION
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "database" / "retailiq.db"

@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM master_sales_dataset",
        conn
    )

    conn.close()

    return df

df = load_data()

# ==========================================================
# DATA PREPARATION
# ==========================================================

df["order_purchase_timestamp"] = pd.to_datetime(
    df["order_purchase_timestamp"]
)

# ==========================================================
# SIDEBAR FILTERS
# ==========================================================

st.sidebar.header("Dashboard Filters")

# ---------------- YEAR ----------------

years = sorted(df["purchase_year"].dropna().unique())

selected_years = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

df = df[df["purchase_year"].isin(selected_years)]

# ---------------- STATE ----------------

states = sorted(df["customer_state"].dropna().unique())

selected_states = st.sidebar.multiselect(
    "Customer State",
    states,
    default=states
)

df = df[df["customer_state"].isin(selected_states)]

# ---------------- REVIEW ----------------

reviews = sorted(df["review_score"].dropna().unique())

selected_reviews = st.sidebar.multiselect(
    "Review Score",
    reviews,
    default=reviews
)

df = df[df["review_score"].isin(selected_reviews)]

# ==========================================================
# KPI CALCULATIONS
# ==========================================================

total_revenue = df["price"].sum()

total_orders = df["order_id"].nunique()

total_customers = df["customer_unique_id"].nunique()

avg_order_value = total_revenue / total_orders

avg_review = df["review_score"].mean()

avg_delivery = df["delivery_days"].mean()

# ==========================================================
# KPI CARDS
# ==========================================================

st.subheader("Executive KPIs")

c1, c2, c3, c4, c5, c6 = st.columns(6)

c1.metric(
    "💰 Revenue",
    f"${total_revenue:,.2f}"
)

c2.metric(
    "📦 Orders",
    f"{total_orders:,}"
)

c3.metric(
    "👥 Customers",
    f"{total_customers:,}"
)

c4.metric(
    "🛒 Avg Order",
    f"${avg_order_value:,.2f}"
)

c5.metric(
    "⭐ Rating",
    f"{avg_review:.2f}"
)

c6.metric(
    "🚚 Delivery",
    f"{avg_delivery:.1f} Days"
)

st.divider()

# ==========================================================
# CHART DATA
# ==========================================================

monthly_sales = (
    df.groupby("purchase_month")["price"]
    .sum()
    .reset_index()
)

category_sales = (
    df.groupby("product_category_name_english")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

seller_sales = (
    df.groupby("seller_id")["price"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

state_sales = (
    df.groupby("customer_state")["price"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

payment_sales = (
    df.groupby("payment_type")["payment_value"]
    .sum()
    .reset_index()
)

# ==========================================================
# CREATE CHARTS
# ==========================================================

revenue_chart = px.line(
    monthly_sales,
    x="purchase_month",
    y="price",
    title="Monthly Revenue Trend",
    markers=True
)

category_chart = px.bar(
    category_sales,
    x="price",
    y="product_category_name_english",
    orientation="h",
    title="Top 10 Product Categories"
)

seller_chart = px.bar(
    seller_sales,
    x="price",
    y="seller_id",
    orientation="h",
    title="Top 10 Sellers"
)

state_chart = px.bar(
    state_sales,
    x="customer_state",
    y="price",
    title="Revenue by Customer State"
)

payment_chart = px.pie(
    payment_sales,
    names="payment_type",
    values="payment_value",
    title="Payment Method Distribution"
)

review_chart = px.histogram(
    df,
    x="review_score",
    nbins=5,
    title="Review Score Distribution"
)

delivery_chart = px.histogram(
    df,
    x="delivery_days",
    nbins=30,
    title="Delivery Days Distribution"
)

# ==========================================================
# DASHBOARD LAYOUT
# ==========================================================

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.plotly_chart(
        revenue_chart,
        use_container_width=True
    )

with row1_col2:
    st.plotly_chart(
        category_chart,
        use_container_width=True
    )

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.plotly_chart(
        seller_chart,
        use_container_width=True
    )

with row2_col2:
    st.plotly_chart(
        state_chart,
        use_container_width=True
    )

row3_col1, row3_col2 = st.columns(2)

with row3_col1:
    st.plotly_chart(
        payment_chart,
        use_container_width=True
    )

with row3_col2:
    st.plotly_chart(
        review_chart,
        use_container_width=True
    )

st.plotly_chart(
    delivery_chart,
    use_container_width=True
)

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "RetailIQ Analytics Dashboard | Built with Streamlit, Plotly, SQLite & Python"
)