import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Customer Lifetime Value",
    page_icon="💰",
    layout="wide"
)

st.title("💰 Customer Lifetime Value Prediction")
st.markdown("---")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("data/customer_clv_predictions.csv")

df = load_data()

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

total_customers = len(df)
average_clv = df["PREDICTED_CLV"].mean()
highest_clv = df["PREDICTED_CLV"].max()
average_revenue = df["TOTAL_REVENUE"].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Customers",
    f"{total_customers:,}"
)

col2.metric(
    "Average Predicted CLV",
    f"${average_clv:,.2f}"
)

col3.metric(
    "Highest Predicted CLV",
    f"${highest_clv:,.2f}"
)

col4.metric(
    "Average Revenue",
    f"${average_revenue:,.2f}"
)

st.markdown("---")

# --------------------------------------------------
# Customer Search
# --------------------------------------------------

customer = st.selectbox(
    "Select Customer",
    sorted(df["CUSTOMER_KEY"].unique())
)

customer_df = df[df["CUSTOMER_KEY"] == customer]

st.subheader("Customer Details")

st.dataframe(customer_df)

st.markdown("---")

# --------------------------------------------------
# Top 20 Customers
# --------------------------------------------------

st.subheader("Top 20 Customers by Predicted CLV")

top20 = (
    df.sort_values(
        "PREDICTED_CLV",
        ascending=False
    )
    .head(20)
)

st.dataframe(top20)

st.markdown("---")

# --------------------------------------------------
# CLV Distribution
# --------------------------------------------------

fig = px.histogram(
    df,
    x="PREDICTED_CLV",
    nbins=40,
    title="Predicted Customer Lifetime Value Distribution"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Revenue vs Predicted CLV
# --------------------------------------------------

fig = px.scatter(
    df,
    x="TOTAL_REVENUE",
    y="PREDICTED_CLV",
    color="TOTAL_ORDERS",
    size="TOTAL_ITEMS",
    hover_data=["CUSTOMER_KEY"],
    title="Revenue vs Predicted CLV"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Feature Importance
# --------------------------------------------------

st.subheader("Feature Importance")

feature_importance = pd.read_csv(
    "data/clv_feature_importance.csv"
)

fig = px.bar(
    feature_importance,
    x="Importance",
    y="Feature",
    orientation="h",
    title="Feature Importance"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.success("Customer Lifetime Value Dashboard Loaded Successfully!")