"""
Module 2 & 4: Data Cleaning + Feature Engineering
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Drops fully empty rows
    - Fills missing numeric values with column median
    - Fills missing categorical values with mode
    - Removes duplicate CustomerIDs if present
    """
    df = df.copy()
    df = df.dropna(how="all")

    if "CustomerID" in df.columns:
        df = df.drop_duplicates(subset="CustomerID")

    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        if df[col].isna().any():
            df[col] = df[col].fillna(df[col].median())

    categorical_cols = df.select_dtypes(include="object").columns
    for col in categorical_cols:
        if df[col].isna().any():
            mode_val = df[col].mode()
            if not mode_val.empty:
                df[col] = df[col].fillna(mode_val[0])

    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a couple of derived features useful for segmentation, if the
    relevant source columns exist. Safe no-ops otherwise.
    """
    df = df.copy()

    if "TotalPurchaseValue" in df.columns and "TotalOrders" in df.columns:
        df["AvgOrderValue"] = df["TotalPurchaseValue"] / df["TotalOrders"].replace(0, np.nan)
        df["AvgOrderValue"] = df["AvgOrderValue"].fillna(0)

    if "LastPurchaseDate" in df.columns:
        try:
            last_dates = pd.to_datetime(df["LastPurchaseDate"], errors="coerce")
            reference_date = last_dates.max()
            df["RecencyDays"] = (reference_date - last_dates).dt.days
            df["RecencyDays"] = df["RecencyDays"].fillna(df["RecencyDays"].median())
        except Exception:
            pass

    # Kaggle "Mall Customer Segmentation" dataset support: Annual Income (k$)
    # and Spending Score (1-100) are already the core segmentation features.
    # Add Income-per-Age as a simple extra behavioral feature when present.
    if "Annual Income (k$)" in df.columns and "Age" in df.columns:
        df["IncomePerAge"] = (df["Annual Income (k$)"] / df["Age"]).round(2)

    return df


def scale_features(df: pd.DataFrame, feature_cols: list):
    """
    Standardizes chosen feature columns (mean=0, std=1) for K-Means,
    since K-Means is distance-based and sensitive to feature scale.
    Returns (scaled_array, fitted_scaler).
    """
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[feature_cols])
    return scaled, scaler
