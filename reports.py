"""
Module 7: Business Report Generation
"""

import pandas as pd
from datetime import datetime


def generate_segment_summary(df: pd.DataFrame, segment_col: str, numeric_cols: list) -> pd.DataFrame:
    """Returns a per-segment summary table (count + average metrics)."""
    summary = df.groupby(segment_col)[numeric_cols].mean().round(2)
    summary["CustomerCount"] = df[segment_col].value_counts()
    summary = summary.reset_index()
    return summary


def generate_text_report(df: pd.DataFrame, segment_col: str, recommendation_fn) -> str:
    """Builds a plain-text business insights report."""
    lines = []
    lines.append("E-COMMERCE CUSTOMER SEGMENTATION - BUSINESS INSIGHTS REPORT")
    lines.append(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Total Customers Analyzed: {len(df)}")
    lines.append(f"Number of Segments: {df[segment_col].nunique()}")
    lines.append("")

    income_col = next((c for c in ["Annual Income (k$)", "AnnualIncome_k"] if c in df.columns), None)
    spend_col = next((c for c in ["Spending Score (1-100)", "SpendingScore"] if c in df.columns), None)
    orders_col = next((c for c in ["TotalOrders"] if c in df.columns), None)
    age_col = "Age" if "Age" in df.columns else None

    for segment in sorted(df[segment_col].unique()):
        sub = df[df[segment_col] == segment]
        lines.append(f"Segment: {segment}")
        lines.append(f"  Customer Count: {len(sub)} ({len(sub)/len(df)*100:.1f}% of total)")
        if age_col:
            lines.append(f"  Avg Age: {sub[age_col].mean():.1f}")
        if income_col:
            lines.append(f"  Avg Annual Income: {sub[income_col].mean():.1f}k")
        if spend_col:
            lines.append(f"  Avg Spending Score: {sub[spend_col].mean():.1f}")
        if orders_col:
            lines.append(f"  Avg Total Orders: {sub[orders_col].mean():.1f}")
        lines.append(f"  Recommended Action: {recommendation_fn(segment)}")
        lines.append("")

    return "\n".join(lines)


def export_results_csv(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)
    return path
