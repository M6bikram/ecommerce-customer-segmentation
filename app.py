"""
E-Commerce Customer Segmentation - Main Streamlit Application by Bikram Mondal

"""

import streamlit as st
import pandas as pd
import os

from upload import load_dataset, validate_dataset
from preprocessing import clean_data, engineer_features, scale_features
from clustering import (
    compute_elbow_and_silhouette, suggest_best_k, run_kmeans,
    label_segments, business_recommendation
)
from visualization import (
    plot_distribution, plot_elbow, plot_silhouette,
    plot_clusters_2d, plot_segment_counts, plot_segment_avg_metrics
)
from reports import generate_segment_summary, generate_text_report, export_results_csv

st.set_page_config(page_title="E-Commerce Customer Segmentation", layout="wide")

st.title("E-Commerce Customer Segmentation Dashboard by Bikram Mondal")
st.caption("Unsupervised ML project: K-Means clustering on customer purchasing behavior")

# ---------------------------------------------------------------
# Screen 1: Dataset Upload
# ---------------------------------------------------------------
st.sidebar.header("1. Dataset Upload")
uploaded_file = st.sidebar.file_uploader("Upload customer CSV", type=["csv"])
dataset_choice = st.sidebar.radio(
    "Sample Dataset",
    ["Kaggle: Mall Customer Segmentation (real, 200 rows)", "Sample Customer Dataset (400 rows)"],
    index=0,
)

if uploaded_file is not None:
    raw_df = load_dataset(uploaded_file)
elif dataset_choice.startswith("Kaggle"):
    sample_path = os.path.join("datasets", "Mall_Customers.csv")
    raw_df = load_dataset(sample_path)
    st.sidebar.caption(
        "Source: Kaggle Customer Segmentation Dataset — "
        "https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python"
    )
else:
    sample_path = os.path.join("datasets", "sample_customer_data.csv")
    raw_df = load_dataset(sample_path)

validation = validate_dataset(raw_df)
if not validation["is_valid"]:
    st.error(validation["message"])
    st.stop()
else:
    st.sidebar.success(validation["message"])

# ---------------------------------------------------------------
# Screen 2: Customer Overview + Cleaning
# ---------------------------------------------------------------
st.header("📋Customer Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Total Customers", raw_df.shape[0])
col2.metric("Columns", raw_df.shape[1])
col3.metric("Missing Values", int(raw_df.isna().sum().sum()))

with st.expander("View Original Dataset"):
    st.dataframe(raw_df.head(20))

clean_df = clean_data(raw_df)
featured_df = engineer_features(clean_df)

with st.expander("View cleaned & feature-engineered dataset"):
    st.dataframe(featured_df.head(20))
    st.caption("Missing values filled with median/mode.")

# ---------------------------------------------------------------
# Screen 3: Exploratory Data Analysis
# ---------------------------------------------------------------
st.header("📊Exploratory Data Analysis")
numeric_cols_all = featured_df.select_dtypes(include="number").columns.tolist()
numeric_cols_all = [c for c in numeric_cols_all if c != "CustomerID"]

eda_col = st.selectbox("Select a column to view its distribution", numeric_cols_all)
st.plotly_chart(plot_distribution(featured_df, eda_col), use_container_width=True)

# ---------------------------------------------------------------
# Screen 4: Feature Selection for Clustering
# ---------------------------------------------------------------
st.header("⚙️ Feature Selection & Clustering Setup")

preferred_pairs = [
    ["Annual Income (k$)", "Spending Score (1-100)"],  # Kaggle Mall Customers dataset
    ["AnnualIncome_k", "SpendingScore"],                 # sample_customer_dataset
]
default_features = []
for pair in preferred_pairs:
    if all(c in numeric_cols_all for c in pair):
        default_features = pair
        break
if not default_features:
    default_features = numeric_cols_all[:2]

feature_cols = st.multiselect(
    "Select numeric features to use for clustering",
    options=numeric_cols_all,
    default=default_features,
)

if len(feature_cols) < 2:
    st.warning("Please select at least 2 features to proceed with clustering.")
    st.stop()

scaled_data, scaler = scale_features(featured_df, feature_cols)

# ---------------------------------------------------------------
# Screen 5: Elbow Method + Silhouette Score
# ---------------------------------------------------------------
st.subheader("Determining the Optimal Number of Clusters")
metrics_df = compute_elbow_and_silhouette(scaled_data, k_range=range(2, 9))
best_k = suggest_best_k(metrics_df)

c1, c2 = st.columns(2)
c1.plotly_chart(plot_elbow(metrics_df), use_container_width=True)
c2.plotly_chart(plot_silhouette(metrics_df), use_container_width=True)

st.info(f"💡 Suggested optimal k (highest silhouette score): **{best_k}**")

chosen_k = st.slider("Choose number of clusters (k)", min_value=2, max_value=8, value=best_k)

# ---------------------------------------------------------------
# Screen 6: Run K-Means & Label Segments
# ---------------------------------------------------------------
labels, model = run_kmeans(scaled_data, chosen_k)
result_df = featured_df.copy()
result_df["Cluster"] = labels

income_candidates = ["Annual Income (k$)", "AnnualIncome_k"]
spend_candidates = ["Spending Score (1-100)", "SpendingScore"]
income_col = next((c for c in income_candidates if c in result_df.columns), feature_cols[0])
spend_col = next((c for c in spend_candidates if c in result_df.columns), feature_cols[min(1, len(feature_cols)-1)])
result_df = label_segments(result_df, "Cluster", income_col, spend_col)

st.header("🎯 Customer Segments")
x_axis = st.selectbox("X-axis for cluster plot", feature_cols, index=0)
y_axis = st.selectbox("Y-axis for cluster plot", feature_cols, index=min(1, len(feature_cols)-1))

st.plotly_chart(plot_clusters_2d(result_df, x_axis, y_axis), use_container_width=True)

col1, col2 = st.columns(2)
col1.plotly_chart(plot_segment_counts(result_df), use_container_width=True)
col2.plotly_chart(plot_segment_avg_metrics(result_df, "Segment", feature_cols), use_container_width=True)

# ---------------------------------------------------------------
# Screen 7: Business Insights & Report
# ---------------------------------------------------------------
st.header("💡 Business Insights")
summary_table = generate_segment_summary(result_df, "Segment", feature_cols)
st.dataframe(summary_table)

for segment in sorted(result_df["Segment"].unique()):
    st.markdown(f"**{segment}** → {business_recommendation(segment)}")

st.header("📥 Export Results")
os.makedirs("outputs", exist_ok=True)
csv_path = export_results_csv(result_df, "outputs/segmented_customers.csv")

with open(csv_path, "rb") as f:
    st.download_button("Download Segmented Customer Data (CSV)", f, file_name="segmented_customers.csv")

report_text = generate_text_report(result_df, "Segment", business_recommendation)
st.download_button("Download Business Insights Report (TXT)", report_text, file_name="business_insights_report.txt")

with st.expander("Preview text report"):
    st.text(report_text)
