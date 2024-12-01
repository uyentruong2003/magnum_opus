print("Hello World!")
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt
import seaborn as sns


# Load data
df = pd.read_csv('MASTER_FILE_OF_OCCURRENCE_FREQUENCE_AND_CASUALTY_SUMMARY.csv')

# Preprocess: Standardize features
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df.iloc[:, 1:])  # Assuming the first column is 'County'
scaled_data = np.nan_to_num(scaled_data, nan=0.0) # replace any NaN value with 0

print("Any NaN values in data?", np.isnan(scaled_data).any())
print("Any infinite values in data?", np.isinf(scaled_data).any())

# Perform hierarchical clustering
linkage_matrix = linkage(scaled_data, method='ward', metric='euclidean')

# Plot dendrogram
plt.figure(figsize=(10, 7))
dendrogram(linkage_matrix, labels=df['County'].values, leaf_rotation=90)
plt.title('Dendrogram')
plt.xlabel('Counties')
plt.ylabel('Distance')
plt.show()

# Cut dendrogram into clusters
clusters = fcluster(linkage_matrix, t=5, criterion='maxclust')  # Change t as needed
df['Cluster'] = clusters

# Plot Cluster Map
# Create a DataFrame for the heatmap with counties as row labels
clustered_df = pd.DataFrame(scaled_data, index=df['County'], columns=df.columns[1:])

# Plot using seaborn's clustermap
sns.clustermap(
    clustered_df,
    method='ward',  # Linkage method
    metric='euclidean',  # Distance metric
    figsize=(12, 10),
    cmap='viridis',  # Color map
    standard_scale=1,  # Normalize data (columns)
    row_cluster=True,  # Enable row clustering
    col_cluster=False  # Disable column clustering to focus on counties
)

plt.title('Cluster Map of Alabama Counties')
plt.show()

# Save or inspect results
df.to_csv('clustered_counties.csv', index=False)
print(df[['County', 'Cluster']].head())
