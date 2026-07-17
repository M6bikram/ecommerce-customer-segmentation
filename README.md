# E-Commerce Customer Segmentation

Machine Learning project that segments e-commerce customers into meaningful
groups using K-Means clustering, with an interactive Streamlit dashboard.

## Project Structure
```
E-Commerce-Customer-Segmentation/
├── app.py              # Main Streamlit dashboard
├── upload.py           # Module 1: Dataset upload & validation
├── preprocessing.py    # Module 2 & 4: Cleaning + feature engineering
├── clustering.py       # Module 5: K-Means clustering, elbow, silhouette
├── visualization.py    # Module 6: Plotly charts
├── reports.py          # Module 7: Business report generation
├── database.py         # Optional: SQLite storage
├── requirements.txt
├── datasets/
│   └── sample_customer_data.csv
├── outputs/             # Generated CSVs / reports land here
└── README.md
```

## How to Run

1. Install Python 3.11+ and create a virtual environment (recommended):
   ```
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the dashboard:
   ```
   streamlit run app.py
   ```

4. Your browser will open at `http://localhost:8501`. In the sidebar
   you can choose:
   - **Kaggle: Mall Customer Segmentation (real, 200 rows)** — the
     actual dataset from Kaggle, bundled at `datasets/Mall_Customers.csv`
     (default, selected automatically)
   - **Synthetic sample (400 rows)** — a generated fallback dataset
   - Or upload your own CSV

## Dataset Used

**Mall Customer Segmentation Data**
Kaggle link: https://www.kaggle.com/datasets/vjchoudhary7/customer-segmentation-tutorial-in-python

This is the real dataset (not synthetic) — 200 mall customers with
`CustomerID, Gender, Age, Annual Income (k$), Spending Score (1-100)`.
It's the most widely used beginner dataset for K-Means customer
segmentation tutorials, which makes it a safe, well-documented choice
for an assignment — your results (best k, cluster shapes) will match
what's commonly shown in reference tutorials, so it's easy to verify
your work is correct.

A copy is already bundled at `datasets/Mall_Customers.csv` so the app
runs offline without needing a Kaggle account/API key.

## What the Dashboard Does

1. **Upload & Validate** — reads your CSV and checks it has usable numeric columns.
2. **Customer Overview** — quick stats (row count, missing values).
3. **Data Cleaning** — fills missing values (median/mode), removes duplicates.
4. **Feature Engineering** — derives Average Order Value and Recency (days since last purchase).
5. **EDA** — histogram of any selected numeric column.
6. **Clustering Setup** — pick which features to cluster on.
7. **Elbow Method + Silhouette Score** — helps you (and the model) pick the best k.
8. **K-Means Segmentation** — clusters customers, then auto-labels each
   cluster (e.g. "High-Value Loyalists", "Budget Enthusiasts") based on
   relative income/spending.
9. **Business Insights** — per-segment averages and a recommended marketing action.
10. **Export** — download the segmented dataset (CSV) and a plain-text business report.

## Dataset Fields Used
`CustomerID, Age, Gender, AnnualIncome_k, SpendingScore, TotalOrders,
TotalPurchaseValue, PurchaseFrequency_per_month, LastPurchaseDate`

You can swap in a real Kaggle dataset — the app only needs at least
2 numeric columns to work; if your column names differ, just select
them manually in the "Feature Selection" step.

## Notes for Viva / Submission
See `VIVA_QUESTIONS_AND_ANSWERS.md` for prepared answers to the 10
viva questions listed in the project brief.
