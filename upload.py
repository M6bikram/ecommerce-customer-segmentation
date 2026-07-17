"""
Module 1: Dataset Upload & Validation
Handles reading the uploaded CSV and checking that it has usable columns.
"""

import pandas as pd

REQUIRED_NUMERIC_CANDIDATES = [
    "AnnualIncome_k", "SpendingScore", "TotalOrders",
    "TotalPurchaseValue", "PurchaseFrequency_per_month", "Age"
]


def load_dataset(file) -> pd.DataFrame:
    """Load a CSV file (path or file-like object) into a DataFrame."""
    df = pd.read_csv(file)
    df.columns = [c.strip() for c in df.columns]
    return df


def validate_dataset(df: pd.DataFrame) -> dict:
    """
    Basic validation: checks the file isn't empty, and that at least
    two numeric columns exist that can be used for clustering.
    Returns a dict with 'is_valid', 'message', and 'usable_numeric_cols'.
    """
    if df.empty:
        return {"is_valid": False, "message": "Uploaded file is empty.", "usable_numeric_cols": []}

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if len(numeric_cols) < 2:
        return {
            "is_valid": False,
            "message": "Dataset needs at least 2 numeric columns (e.g. Income, Spending Score) for clustering.",
            "usable_numeric_cols": numeric_cols,
        }

    return {
        "is_valid": True,
        "message": f"Dataset validated successfully. {df.shape[0]} rows, {df.shape[1]} columns.",
        "usable_numeric_cols": numeric_cols,
    }
