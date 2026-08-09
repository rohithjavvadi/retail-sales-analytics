# RetailIQ Analytics Platform

RetailIQ is an end-to-end retail analytics platform designed to transform transactional sales data into actionable business insights.

The project combines data engineering, cloud data warehousing, business analytics, customer analytics, machine learning, and interactive dashboards into a single analytics platform.

---

## Business Objective

Retail businesses generate large volumes of transactional data, but raw transaction records alone do not provide clear answers to important business questions.

RetailIQ focuses on answering questions such as:

- How much revenue is the business generating?
- How many orders and customers are being served?
- What is the average order value?
- Which product categories generate the most revenue?
- Which states generate the most sales?
- Which sellers contribute the most revenue?
- What is the expected lifetime value of customers?

---

## Architecture

```text
                 Retail Transaction Data
                         │
                         ▼
                  Data Preparation
                         │
                         ▼
                    AWS / Storage
                         │
                         ▼
                  Snowflake Warehouse
                         │
                         ▼
                SQL Analytics Layer
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       Business Analytics      Customer Analytics
              │                     │
              ▼                     ▼
       Sales Analytics       Customer Lifetime Value
              │                     │
              └──────────┬──────────┘
                         ▼
                  Streamlit Platform
                         │
                         ▼
                Business Insights

🛠️ Technology Stack
Data & Cloud
Python
SQL
Snowflake
AWS S3
Boto3
Analytics & Machine Learning
Pandas
NumPy
Scikit-learn
Prophet
SciPy
Visualization & Application
Plotly
Streamlit
Development
Git
GitHub
Python Virtual Environment
📊 Current Dashboards
Sales Analytics

The Sales Analytics dashboard connects to Snowflake through the VW_MASTER_SALES view and provides:

Total Revenue
Total Orders
Total Customers
Average Order Value
Monthly Revenue Trend
Top 10 Product Categories
Revenue by Customer State
Top 10 Sellers
Detailed Sales Data
CSV Export
Customer Lifetime Value

The CLV dashboard analyzes customer purchasing behavior to estimate customer lifetime value and support customer-focused business decisions.

❄️ Snowflake Integration

Snowflake is used as the analytical data warehouse.

The application uses a reusable connection module:

snowflake_connection.py

Sales Analytics retrieves data using:

SELECT *
FROM VW_MASTER_SALES
📁 Project Structure
realsalesanalytics/
│
├── dashboards/
│   ├── app.py
│   └── pages/
│       ├── 1_📊_Sales_Analytics.py
│       └── 5_💰_Customer_Lifetime_Value.py
│
├── notebooks/
├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── database/
├── snowflake_connection.py
├── requirements.txt
├── .gitignore
└── README.md
🚀 Setup
1. Clone the repository
git clone <your-github-repository-url>
cd realsalesanalytics
2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate
3. Install dependencies
pip install -r requirements.txt
4. Configure Snowflake

Create a .env file with your Snowflake credentials.

Do not commit .env to GitHub.

5. Run the application
streamlit run dashboards/app.py
🔮 Future Enhancements

Planned enhancements include:

Sales forecasting dashboard
Customer segmentation dashboard
Product recommendation dashboard
Customer churn prediction
Data quality validation
Airflow orchestration
dbt transformations
GitHub Actions CI/CD
Docker deployment
AI-powered business assistant
📌 Project Status

Current Status: Active Development

Completed:

Data analytics workflows
Snowflake integration
Sales Analytics dashboard
Customer Lifetime Value analysis
Streamlit application
Git/GitHub project structure
👤 Author

Rohith Javvadi
MS Data Analytics Engineering
George Mason University


