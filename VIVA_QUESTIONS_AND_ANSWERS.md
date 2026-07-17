# Viva Questions & Answers

**1. What is customer segmentation?**
Customer segmentation is the process of dividing a customer base into
groups of individuals who share similar characteristics — such as
income, spending behavior, or purchase frequency — so a business can
target each group with tailored marketing, pricing, or product
recommendations instead of treating all customers the same way.

**2. Why is K-Means used?**
K-Means is simple, fast, and scales well to large datasets. It works
well when clusters are roughly spherical and separated by distance,
which fits typical income/spending-based customer data. It's also easy
to interpret — each cluster gets a centroid you can describe in plain
business terms — and it's the industry-standard baseline for this kind
of unsupervised segmentation task.

**3. What is the Elbow Method?**
It's a technique for choosing the number of clusters (k). You run
K-Means for a range of k values and plot the "inertia" (within-cluster
sum of squared distances) against k. As k increases, inertia always
decreases, but the rate of decrease slows down after the "true" number
of clusters — the plot bends like an elbow at that point, indicating a
good tradeoff between simplicity and fit.

**4. Explain the Silhouette Score.**
The silhouette score measures how well each point fits within its own
cluster compared to the nearest neighboring cluster. It ranges from -1
to 1: values near 1 mean the point is well-matched to its own cluster
and poorly matched to others (good clustering), values near 0 mean
clusters overlap, and negative values suggest points may be in the
wrong cluster. Averaging this across all points gives a single score
used to compare different k values objectively — in this project it's
used alongside the elbow method to pick the best k.

**5. What is feature scaling?**
Feature scaling transforms numeric features so they're on comparable
scales — for example, standardization rescales each feature to have
mean 0 and standard deviation 1. This project uses `StandardScaler`
before clustering because K-Means relies on Euclidean distance, and
without scaling, a feature like "Total Purchase Value" (in thousands)
would dominate the distance calculation over a feature like "Age",
distorting the clusters.

**6. Why is data preprocessing important?**
Raw data almost always has missing values, duplicates, or
inconsistent formats. If left unhandled, these can bias the model,
break calculations, or produce misleading clusters. Preprocessing
(cleaning + feature engineering) ensures the data going into the model
is complete, consistent, and represents customer behavior accurately —
which directly affects clustering quality.

**7. How does clustering help businesses?**
It turns a large, undifferentiated customer base into a small number
of actionable groups. Instead of one generic marketing campaign,
a business can identify — for example — high-value loyal customers
worth retention offers, versus low-engagement customers who need
win-back campaigns, versus price-sensitive high earners who respond to
discounts. This improves marketing ROI, customer retention, and
resource allocation.

**8. Difference between supervised and unsupervised learning?**
Supervised learning trains on labeled data (each input has a known,
correct output) to predict outcomes for new inputs — e.g. predicting
whether a customer will churn, given historical churn labels.
Unsupervised learning works on unlabeled data and finds hidden
structure on its own — e.g. K-Means groups customers into clusters
without ever being told what the "correct" groups are. This project
is unsupervised since no segment labels exist beforehand; the model
discovers the groups from the data itself.

**9. How can this project be improved?**
- Add RFM (Recency, Frequency, Monetary) analysis as additional features
- Try other algorithms (DBSCAN, Hierarchical Clustering, Gaussian Mixture Models) and compare
- Add a customer churn prediction module (supervised learning) on top of segments
- Deploy to the cloud for real-time use instead of local-only
- Integrate with a live CRM/database instead of static CSV uploads
- Add PCA for visualizing clusters when more than 2-3 features are used

**10. What challenges did you face?**
Common, honest challenges to mention: choosing the right number of
clusters objectively (solved using elbow + silhouette rather than
guessing), handling missing/inconsistent data before clustering, and
deciding how to translate abstract cluster numbers (Cluster 0, 1, 2...)
into business-meaningful segment names that a non-technical
stakeholder could act on.
