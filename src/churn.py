import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

from snowflake.snowpark import Session

connection_parameters = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER"),
    "password": os.getenv("SNOWFLAKE_PASSWORD"),
    "role": os.getenv("SNOWFLAKE_ROLE"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
    "database": os.getenv("SNOWFLAKE_DATABASE"),
    "schema": os.getenv("SNOWFLAKE_SCHEMA")
}

session = Session.builder.configs(connection_parameters).create()

print("✅ Connected to Snowflake")

fact_sales = session.table("FACT_SALES").to_pandas()
dim_customers = session.table("DIM_CUSTOMERS").to_pandas()

print(fact_sales.columns.tolist())
print()
print(dim_customers.columns.tolist())

print(fact_sales.head())


# ==========================================
# Build Customer CLV Dataset
# ==========================================

# Load DIM_DATE
dim_date = session.table("DIM_DATE").to_pandas()

# Convert FULL_DATE to datetime
dim_date["FULL_DATE"] = pd.to_datetime(dim_date["FULL_DATE"])

# Merge FACT_SALES with DIM_DATE
sales = fact_sales.merge(
    dim_date[["DATE_KEY", "FULL_DATE"]],
    on="DATE_KEY",
    how="left"
)

# Reference date (latest purchase date)
reference_date = sales["FULL_DATE"].max()

# Aggregate customer-level features
customer_clv = (
    sales.groupby("CUSTOMER_KEY")
    .agg(
        TOTAL_ORDERS=("ORDER_ID", "nunique"),
        TOTAL_REVENUE=("PAYMENT_VALUE", "sum"),
        TOTAL_PRICE=("PRICE", "sum"),
        TOTAL_FREIGHT=("FREIGHT_VALUE", "sum"),
        AVG_ORDER_VALUE=("PAYMENT_VALUE", "mean"),
        TOTAL_ITEMS=("ORDER_ITEM_ID", "count"),
        AVG_ITEM_PRICE=("PRICE", "mean"),
        LAST_PURCHASE=("FULL_DATE", "max")
    )
    .reset_index()
)

# Recency
customer_clv["RECENCY"] = (
    reference_date - customer_clv["LAST_PURCHASE"]
).dt.days

# Frequency & Monetary
customer_clv["FREQUENCY"] = customer_clv["TOTAL_ORDERS"]
customer_clv["MONETARY"] = customer_clv["TOTAL_REVENUE"]

# Remove helper column
customer_clv.drop(columns=["LAST_PURCHASE"], inplace=True)

print("=" * 60)
print("Customer CLV Dataset Shape")
print(customer_clv.shape)

print("\nFirst 10 Customers")
print(customer_clv.head(10))

print("\nMissing Values")
print(customer_clv.isnull().sum())

# =====================================================
# Create Future CLV Target
# =====================================================

# Sort by purchase date
sales = sales.sort_values("FULL_DATE")

# Find cutoff date (75% through the timeline)
cutoff_date = sales["FULL_DATE"].quantile(0.75)

print("Cutoff Date:", cutoff_date)

# Observation period
observation = sales[sales["FULL_DATE"] <= cutoff_date].copy()

# Prediction period
future = sales[sales["FULL_DATE"] > cutoff_date].copy()

print("\nObservation Rows:", observation.shape)
print("Future Rows:", future.shape)

# =====================================================
# Historical Customer Features
# =====================================================

reference_date = observation["FULL_DATE"].max()

historical_features = (
    observation.groupby("CUSTOMER_KEY")
    .agg(
        TOTAL_ORDERS=("ORDER_ID", "nunique"),
        TOTAL_REVENUE=("PAYMENT_VALUE", "sum"),
        AVG_ORDER_VALUE=("PAYMENT_VALUE", "mean"),
        TOTAL_ITEMS=("ORDER_ITEM_ID", "count"),
        LAST_PURCHASE=("FULL_DATE", "max")
    )
    .reset_index()
)

historical_features["RECENCY"] = (
    reference_date - historical_features["LAST_PURCHASE"]
).dt.days

historical_features.drop(columns="LAST_PURCHASE", inplace=True)

print(historical_features.shape)
historical_features.head()
# =====================================================
# Future CLV Target
# =====================================================

future_target = (
    future.groupby("CUSTOMER_KEY")
    .agg(
        FUTURE_CLV=("PAYMENT_VALUE", "sum")
    )
    .reset_index()
)

print(future_target.shape)
future_target.head()

# =====================================================
# Final ML Dataset
# =====================================================

clv_dataset = historical_features.merge(
    future_target,
    on="CUSTOMER_KEY",
    how="left"
)

# Customers with no future purchases
clv_dataset["FUTURE_CLV"] = clv_dataset["FUTURE_CLV"].fillna(0)

print("=" * 60)
print(clv_dataset.shape)

print("\nMissing Values")
print(clv_dataset.isnull().sum())

print("\nFirst 10 Customers")
print(clv_dataset.head(10))


# =====================================================
# Customer Lifetime Value Prediction Models
# =====================================================

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import pandas as pd
import numpy as np

# -------------------------
# Features & Target
# -------------------------
X = clv_dataset.drop(columns=["CUSTOMER_KEY", "FUTURE_CLV"])
y = clv_dataset["FUTURE_CLV"]

# -------------------------
# Train-Test Split
# -------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Training Shape :", X_train.shape)
print("Testing Shape  :", X_test.shape)

# -------------------------
# Models
# -------------------------
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    ),
    "Gradient Boosting": GradientBoostingRegressor(
        random_state=42
    )
}

results = []

# -------------------------
# Train & Evaluate
# -------------------------
for name, model in models.items():

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    mae = mean_absolute_error(y_test, predictions)

    rmse = np.sqrt(mean_squared_error(y_test, predictions))

    r2 = r2_score(y_test, predictions)

    results.append({
        "Model": name,
        "MAE": round(mae, 2),
        "RMSE": round(rmse, 2),
        "R2 Score": round(r2, 4)
    })

results_df = pd.DataFrame(results)

print("=" * 60)
print(results_df.sort_values("R2 Score", ascending=False))


import joblib
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
# -----------------------------------------------------
# Create folders
# -----------------------------------------------------

os.makedirs("models", exist_ok=True)
os.makedirs("data", exist_ok=True)
os.makedirs("images", exist_ok=True)

# -----------------------------------------------------
# Train Final Model
# -----------------------------------------------------

best_model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    random_state=42,
    n_jobs=-1,
)

best_model.fit(X_train, y_train)

# -----------------------------------------------------
# Predictions
# -----------------------------------------------------

y_pred = best_model.predict(X_test)

# -----------------------------------------------------
# Evaluation
# -----------------------------------------------------

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("=" * 60)
print("Customer Lifetime Value Model Performance")
print("=" * 60)

print(f"MAE : {mae:.2f}")
print(f"RMSE: {rmse:.2f}")
print(f"R²  : {r2:.4f}")

# -----------------------------------------------------
# Feature Importance
# -----------------------------------------------------

feature_importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": best_model.feature_importances_
}).sort_values(
    by="Importance",
    ascending=False
)

print("\nTop Features")
print(feature_importance)

# -----------------------------------------------------
# Plot Feature Importance
# -----------------------------------------------------

plt.figure(figsize=(10,6))

plt.barh(
    feature_importance["Feature"],
    feature_importance["Importance"]
)

plt.gca().invert_yaxis()

plt.xlabel("Importance")
plt.ylabel("Feature")
plt.title("Customer Lifetime Value Feature Importance")

plt.tight_layout()

plt.savefig(
    "images/clv_feature_importance.png",
    dpi=300
)

plt.show()

# -----------------------------------------------------
# Save Model
# -----------------------------------------------------

joblib.dump(
    best_model,
    "models/clv_model.pkl"
)

# -----------------------------------------------------
# Predict for All Customers
# -----------------------------------------------------

all_predictions = best_model.predict(X)

clv_results = clv_dataset.copy()

clv_results["PREDICTED_CLV"] = all_predictions

# -----------------------------------------------------
# Save Files
# -----------------------------------------------------

clv_dataset.to_csv(
    "data/customer_clv_dataset.csv",
    index=False
)

clv_results.to_csv(
    "data/customer_clv_predictions.csv",
    index=False
)

feature_importance.to_csv(
    "data/clv_feature_importance.csv",
    index=False
)

# -----------------------------------------------------
# Display Top Customers
# -----------------------------------------------------

top_customers = (
    clv_results
    .sort_values(
        "PREDICTED_CLV",
        ascending=False
    )
    .head(20)
)

print("\n" + "=" * 60)
print("Top 20 Customers by Predicted CLV")
print("=" * 60)

print(
    top_customers[
        [
            "CUSTOMER_KEY",
            "TOTAL_REVENUE",
            "TOTAL_ORDERS",
            "RECENCY",
            "PREDICTED_CLV",
        ]
    ]
)

print("\n" + "=" * 60)
print("Files Created Successfully")
print("=" * 60)

print("✔ models/clv_model.pkl")
print("✔ data/customer_clv_dataset.csv")
print("✔ data/customer_clv_predictions.csv")
print("✔ data/clv_feature_importance.csv")
print("✔ images/clv_feature_importance.png")

print("\nDay 18 Completed Successfully!")