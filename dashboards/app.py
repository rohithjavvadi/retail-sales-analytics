import streamlit as st

st.set_page_config(
    page_title="RetailIQ Analytics Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 RetailIQ Analytics Platform")

st.markdown(
    """
    ## Welcome to RetailIQ

    An end-to-end retail analytics platform combining
    **data engineering, business intelligence, machine learning,
    and AI-powered analytics.**
    """
)

st.markdown("---")

# =====================================================
# Platform Overview
# =====================================================

st.subheader("🚀 Analytics Platform")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Analytics", "7")

with col2:
    st.metric("Customers", "98K+")

with col3:
    st.metric("Sales Records", "112K+")

with col4:
    st.metric("ML Models", "4+")

st.markdown("---")

# =====================================================
# Available Modules
# =====================================================

st.subheader("📌 Platform Modules")

col1, col2 = st.columns(2)

with col1:

    st.markdown(
        """
        ### 📊 Sales Analytics
        Analyze revenue, orders, products, sellers, and sales trends.

        ### 📈 Sales Forecasting
        Forecast future sales using historical purchasing patterns.

        ### 🎯 Product Recommendation
        Identify products frequently purchased together and generate recommendations.

        ### 👥 Customer Segmentation
        Segment customers using RFM analysis and K-Means clustering.
        """
    )

with col2:

    st.markdown(
        """
        ### 💰 Customer Lifetime Value
        Predict future customer value and identify high-value customers.

        ### 🚨 Customer Churn
        Identify customers at risk of becoming inactive.

        ### 🤖 AI Business Assistant
        Provide natural-language business insights and analytics.
        """
    )

st.markdown("---")

st.info(
    "👈 Select an analytics module from the sidebar to explore RetailIQ."
)

st.caption(
    "RetailIQ Analytics Platform | Python • Snowflake • Machine Learning • Streamlit"
)