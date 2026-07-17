"""
Module 5: Customer Segmentation using K-Means
Includes Elbow Method, Silhouette Score, Davies-Bouldin Index,
and automatic business-friendly segment naming.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score


def compute_elbow_and_silhouette(scaled_data: np.ndarray, k_range=range(2, 9)):
    """
    Runs K-Means for each k in k_range and records:
    - inertia (for elbow method)
    - silhouette score
    - davies-bouldin index
    Returns a DataFrame indexed by k.
    """
    results = []
    for k in k_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = km.fit_predict(scaled_data)
        inertia = km.inertia_
        sil = silhouette_score(scaled_data, labels) if k > 1 else np.nan
        db = davies_bouldin_score(scaled_data, labels)
        results.append({"k": k, "inertia": inertia, "silhouette_score": sil, "davies_bouldin": db})
    return pd.DataFrame(results)


def suggest_best_k(metrics_df: pd.DataFrame) -> int:
    """Suggests the k with the highest silhouette score."""
    return int(metrics_df.loc[metrics_df["silhouette_score"].idxmax(), "k"])


def run_kmeans(scaled_data: np.ndarray, n_clusters: int):
    """Fits K-Means with chosen number of clusters and returns (labels, model)."""
    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = km.fit_predict(scaled_data)
    return labels, km


def label_segments(df: pd.DataFrame, cluster_col: str, income_col: str, spend_col: str) -> pd.DataFrame:
    """
    Assigns a human-readable business label to each cluster based on
    the cluster's average income and spending score relative to the
    overall dataset average. Adds a 'Segment' column.
    """
    df = df.copy()
    overall_income_mean = df[income_col].mean()
    overall_spend_mean = df[spend_col].mean()

    cluster_profile = df.groupby(cluster_col)[[income_col, spend_col]].mean()

    segment_map = {}
    for cluster_id, row in cluster_profile.iterrows():
        high_income = row[income_col] >= overall_income_mean
        high_spend = row[spend_col] >= overall_spend_mean

        if high_income and high_spend:
            label = "High-Value Loyalists"
        elif high_income and not high_spend:
            label = "Price-Sensitive High Earners"
        elif not high_income and high_spend:
            label = "Budget Enthusiasts"
        else:
            label = "Low Engagement Customers"

        segment_map[cluster_id] = label

    df["Segment"] = df[cluster_col].map(segment_map)
    return df


def business_recommendation(segment: str) -> str:
    """Returns a short marketing recommendation for a given segment label."""
    recommendations = {
        "High-Value Loyalists": "Offer premium loyalty rewards and early access to new products.",
        "Price-Sensitive High Earners": "Use targeted discounts and bundle offers to increase spend.",
        "Budget Enthusiasts": "Promote value deals, flash sales, and frequent small incentives.",
        "Low Engagement Customers": "Send re-engagement campaigns and personalized win-back offers.",
    }
    return recommendations.get(segment, "Analyze further for tailored marketing.")
