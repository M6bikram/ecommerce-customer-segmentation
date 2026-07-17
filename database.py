"""
Optional Module: SQLite storage for customer + cluster results.
Not required for the dashboard to run, but demonstrates the
'Database Design' section of the project (Customer Table, Cluster Table).
"""

import sqlite3
import pandas as pd

DB_PATH = "outputs/segmentation.db"


def save_results_to_db(df: pd.DataFrame, db_path: str = DB_PATH):
    conn = sqlite3.connect(db_path)

    customer_cols = [c for c in ["CustomerID", "Age", "Gender", "AnnualIncome_k", "SpendingScore"] if c in df.columns]
    df[customer_cols].to_sql("Customer", conn, if_exists="replace", index=False)

    cluster_cols = [c for c in ["CustomerID", "Cluster", "Segment"] if c in df.columns]
    if cluster_cols:
        cluster_df = df[cluster_cols].copy()
        cluster_df["Recommendation"] = ""
        cluster_df.to_sql("Cluster", conn, if_exists="replace", index=False)

    conn.close()
    return db_path


def load_table(table_name: str, db_path: str = DB_PATH) -> pd.DataFrame:
    conn = sqlite3.connect(db_path)
    df = pd.read_sql(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df
