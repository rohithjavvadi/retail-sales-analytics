import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


# -----------------------------
# Load RFM Dataset
# -----------------------------
rfm = pd.read_csv("data/external/customer_rfm1.csv")

print("=" * 50)
print("Dataset Preview")
print("=" * 50)
print(rfm.head())

print("\nDataset Shape")
print(rfm.shape)

print("\nColumn Names")
print(rfm.columns)

print("\nData Types")
print(rfm.dtypes)

print("\nMissing Values")
print(rfm.isnull().sum())

print("\nSummary Statistics")
print(rfm.describe())

# -----------------------------
# Convert Date Column
# -----------------------------
rfm["LAST_PURCHASE_DATE"] = pd.to_datetime(
    rfm["LAST_PURCHASE_DATE"]
)

# -----------------------------
# Calculate Recency
# -----------------------------
snapshot_date = rfm["LAST_PURCHASE_DATE"].max() + pd.Timedelta(days=1)

rfm["RECENCY"] = (
    snapshot_date - rfm["LAST_PURCHASE_DATE"]
).dt.days

# -----------------------------
# Keep Only ML Features
# -----------------------------
rfm = rfm[
    [
        "CUSTOMER_UNIQUE_ID",
        "RECENCY",
        "FREQUENCY",
        "MONETARY"
    ]
]
rfm = rfm.drop_duplicates(
    subset="CUSTOMER_UNIQUE_ID"
)
print("\nProcessed Dataset")
print(rfm.head())

print("\nFinal Shape")
print(rfm.shape)

# -----------------------------
# Check Missing Values
# -----------------------------
print("\nMissing Values")
print(rfm.isnull().sum())

# -----------------------------
# Remove Missing Values (if any)
# -----------------------------
rfm = rfm.dropna()

# -----------------------------
# Remove Duplicate Customers
# -----------------------------
rfm = rfm.drop_duplicates(subset="CUSTOMER_UNIQUE_ID")

print("\nShape After Cleaning")
print(rfm.shape)

# -----------------------------
# Features for ML
# -----------------------------
features = rfm[
    [
        "RECENCY",
        "FREQUENCY",
        "MONETARY"
    ]
]

# -----------------------------
# Standard Scaling
# -----------------------------
import numpy as np

# Reduce skewness
rfm["FREQUENCY_LOG"] = np.log1p(rfm["FREQUENCY"])
rfm["MONETARY_LOG"] = np.log1p(rfm["MONETARY"])
scaler = StandardScaler()

scaled_features = scaler.fit_transform(features)

print("\nScaled Feature Shape")
print(scaled_features.shape)

print("\nFirst Five Rows")
print(scaled_features[:5])

# -----------------------------
# Elbow Method
# -----------------------------
wcss = []

cluster_range = range(2, 11)

for k in cluster_range:
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(scaled_features)

    wcss.append(model.inertia_)

# -----------------------------
# Plot Elbow Curve
# -----------------------------
plt.figure(figsize=(8, 5))

plt.plot(
    cluster_range,
    wcss,
    marker="o",
    linewidth=2
)

plt.title("Elbow Method")
plt.xlabel("Number of Clusters (K)")
plt.ylabel("WCSS")

plt.grid(True)

plt.savefig("reports/figures/elbow_method.png")

plt.show()

# -----------------------------
# Final K-Means Model
# -----------------------------
kmeans = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

rfm["CLUSTER"] = kmeans.fit_predict(scaled_features)

print("\nCluster Counts")
print(rfm["CLUSTER"].value_counts().sort_index())

print("\nFirst 10 Customers")
print(rfm.head(10))
# -----------------------------
# Assign Business Segment Names
# -----------------------------
segment_map = {
    0: "Active Customers",
    1: "At-Risk Customers",
    2: "Loyal Customers",
    3: "VIP Customers",
    4: "VIP Customers"   # Merge the outlier into VIP
}

rfm["CUSTOMER_SEGMENT"] = rfm["CLUSTER"].map(segment_map)

print("\nCustomer Segment Counts")
print(rfm["CUSTOMER_SEGMENT"].value_counts())
# -----------------------------
# Cluster Summary
# -----------------------------
cluster_summary = (
    rfm
    .groupby("CLUSTER")[["RECENCY", "FREQUENCY", "MONETARY"]]
    .mean()
    .round(2)
)

print("\nCluster Summary")
print(cluster_summary)

# -----------------------------
# Export Results
# -----------------------------
rfm.to_csv(
    "reports/customer_segments.csv",
    index=False
)

print("\nCustomer segmentation completed successfully!")

# ============================================================
# DAY 17B - CUSTOMER SEGMENT PROFILING
# ============================================================

import pandas as pd
import numpy as np

# ---------------------------------------------
# Average metrics for each cluster
# ---------------------------------------------
cluster_summary = (
    rfm
    .groupby("CLUSTER")
    .agg({
        "RECENCY": "mean",
        "FREQUENCY": "mean",
        "MONETARY": "mean",
        "CUSTOMER_UNIQUE_ID": "count"
    })
    .rename(columns={
        "CUSTOMER_UNIQUE_ID": "CUSTOMERS"
    })
    .round(2)
)

print("=" * 60)
print("CUSTOMER SEGMENT SUMMARY")
print("=" * 60)
print(cluster_summary)

# ---------------------------------------------
# Percentage of customers
# ---------------------------------------------
cluster_summary["PERCENTAGE"] = (
    cluster_summary["CUSTOMERS"] /
    cluster_summary["CUSTOMERS"].sum() * 100
).round(2)

print("\n")
print(cluster_summary.sort_values("CUSTOMERS", ascending=False))

import plotly.express as px

# ---------------------------------------------------
# Customer Count by Segment
# ---------------------------------------------------

segment_counts = (
    rfm["CUSTOMER_SEGMENT"]
    .value_counts()
    .reset_index()
)

segment_counts.columns = [
    "Customer Segment",
    "Customers"
]

fig = px.bar(
    segment_counts,
    x="Customer Segment",
    y="Customers",
    color="Customer Segment",
    text="Customers",
    title="Customer Distribution by Segment"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    template="plotly_white",
    height=600
)

fig.show()

segment_value = (
    rfm.groupby("CUSTOMER_SEGMENT")["MONETARY"]
    .mean()
    .reset_index()
)

fig = px.bar(
    segment_value,
    x="CUSTOMER_SEGMENT",
    y="MONETARY",
    color="CUSTOMER_SEGMENT",
    text_auto=".2f",
    title="Average Customer Spend by Segment"
)

fig.update_layout(
    template="plotly_white",
    height=600,
    xaxis_title="Customer Segment",
    yaxis_title="Average Monetary Value"
)

fig.show()

segment_recency = (
    rfm.groupby("CUSTOMER_SEGMENT")["RECENCY"]
    .mean()
    .reset_index()
)

fig = px.bar(
    segment_recency,
    x="CUSTOMER_SEGMENT",
    y="RECENCY",
    color="CUSTOMER_SEGMENT",
    text_auto=".0f",
    title="Average Recency by Segment"
)

fig.update_layout(
    template="plotly_white",
    height=600,
    xaxis_title="Customer Segment",
    yaxis_title="Days Since Last Purchase"
)

fig.show()
fig = px.scatter(
    rfm,
    x="FREQUENCY",
    y="MONETARY",
    color="CUSTOMER_SEGMENT",
    hover_data=[
        "CUSTOMER_UNIQUE_ID",
        "RECENCY"
    ],
    title="Customer Segmentation Scatter Plot"
)

fig.update_layout(
    template="plotly_white",
    height=700
)

fig.show()
rfm.to_csv(
    "data/processed/customer_segments.csv",
    index=False
)

print("\nFinal customer segmentation dataset saved successfully.")