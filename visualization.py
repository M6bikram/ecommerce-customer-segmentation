"""
Module 6: Visualization helpers (EDA + Cluster plots) using Plotly.
"""

import plotly.express as px
import pandas as pd


def plot_distribution(df: pd.DataFrame, column: str):
    fig = px.histogram(df, x=column, nbins=30, title=f"Distribution of {column}")
    fig.update_layout(bargap=0.05)
    return fig


def plot_elbow(metrics_df: pd.DataFrame):
    fig = px.line(metrics_df, x="k", y="inertia", markers=True,
                   title="Elbow Method for Optimal k")
    fig.update_layout(xaxis_title="Number of Clusters (k)", yaxis_title="Inertia (WCSS)")
    return fig


def plot_silhouette(metrics_df: pd.DataFrame):
    fig = px.line(metrics_df, x="k", y="silhouette_score", markers=True,
                   title="Silhouette Score vs k")
    fig.update_layout(xaxis_title="Number of Clusters (k)", yaxis_title="Silhouette Score")
    return fig


def plot_clusters_2d(df: pd.DataFrame, x_col: str, y_col: str, color_col: str = "Segment"):
    fig = px.scatter(
        df, x=x_col, y=y_col, color=color_col,
        hover_data=[c for c in ["CustomerID", "Age", "Gender"] if c in df.columns],
        title=f"Customer Segments: {x_col} vs {y_col}",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    return fig


def plot_segment_counts(df: pd.DataFrame, segment_col: str = "Segment"):
    counts = df[segment_col].value_counts().reset_index()
    counts.columns = ["Segment", "Count"]
    fig = px.bar(counts, x="Segment", y="Count", color="Segment",
                 title="Customers per Segment",
                 color_discrete_sequence=px.colors.qualitative.Set2)
    return fig


def plot_segment_avg_metrics(df: pd.DataFrame, segment_col: str, metric_cols: list):
    avg_df = df.groupby(segment_col)[metric_cols].mean().reset_index()
    avg_df_melt = avg_df.melt(id_vars=segment_col, var_name="Metric", value_name="Average")
    fig = px.bar(avg_df_melt, x=segment_col, y="Average", color="Metric", barmode="group",
                 title="Average Metrics per Segment")
    return fig
