print("Hello World!")
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D




# Load data
df = pd.read_csv(r"C:\Users\uyenk\OneDrive - The University of Alabama\Self-learning Programming\magnum_opus\MASTER_FILE_OF_SEVERE_WEATHER_INTENSITY_AND_FREQUENCY.csv")

# Preprocess: Standardize features
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df.iloc[:, 2:])  #1st and 2nd colums are 'County' and 'County FIP'
scaled_data = np.nan_to_num(scaled_data, nan=0.0) # replace any NaN value with 0
print("Any NaN values in data?", np.isnan(scaled_data).any())
print("Any infinite values in data?", np.isinf(scaled_data).any())
print("Data type of scaled_data:", scaled_data.dtype)

# Perform hierarchical clustering
linkage_matrix = linkage(scaled_data, method='ward', metric='euclidean')

# Plot dendrogram
plt.figure(figsize=(10, 7))
dendrogram(linkage_matrix, labels=df['County'].values, leaf_rotation=90)
plt.title('Dendrogram')
plt.xlabel('Counties')
plt.ylabel('Distance')
plt.show()


cols_pre_clustering = df.columns[2:]

# Cut dendrogram BY DISTANCE
distance_threshold = 10.0 #specify the distance
clusters = fcluster(linkage_matrix, t=distance_threshold, criterion='distance')  
df['Cluster'] = clusters #add the col 'Cluster' indicating the cluster each county belongs to
# get the unique cluster_id
cluster_ids = df['Cluster'].unique()


# Reduce to 3 components
pca = PCA(n_components=3)
X_3d = pca.fit_transform(scaled_data)

# Add PCA components to the DataFrame
df['PCA1'] = X_3d[:, 0]
df['PCA2'] = X_3d[:, 1]
df['PCA3'] = X_3d[:, 2]

# 3D Scatter plot
fig = plt.figure(figsize=(12, 9))
ax = fig.add_subplot(111, projection='3d')
scatter = ax.scatter(df['PCA1'], df['PCA2'], df['PCA3'], c=df['Cluster'], cmap='tab10', s=50)

ax.set_title('Hierarchical Clustering Visualization (3D PCA)')
ax.set_xlabel('PCA Component 1')
ax.set_ylabel('PCA Component 2')
ax.set_zlabel('PCA Component 3')

# Optional: Add legend for clusters
legend = ax.legend(*scatter.legend_elements(), title="Clusters", loc='upper left')
ax.add_artist(legend)

plt.tight_layout()
plt.show()


# Reduce to 2D using PCA
# pca = PCA(n_components=2)
# X_2d = pca.fit_transform(scaled_data)

# # Add the 2D coordinates to the DataFrame
# df['PCA1'] = X_2d[:, 0]
# df['PCA2'] = X_2d[:, 1]

# # Plot the clusters
# plt.figure(figsize=(12, 8))
# scatter = plt.scatter(df['PCA1'], df['PCA2'], c=df['Cluster'], cmap='tab10', s=60)
            
# plt.title('Hierarchical Clustering Visualization (PCA-reduced)')
# plt.xlabel('PCA Component 1')
# plt.ylabel('PCA Component 2')

# # Optional: add a legend for cluster IDs
# legend1 = plt.legend(*scatter.legend_elements(), title="Clusters", bbox_to_anchor=(1.05, 1), loc='upper left')
# plt.gca().add_artist(legend1)

# plt.tight_layout()
# plt.show()


# # loop thru the unique_ids and filter df by cluster.
# # Save counties to csv by cluster
# for id in cluster_ids:
#     filtered = df[df['Cluster'] == id] #filter by cluster
#     file_name = f"clusters/cluster_{id}.csv" #dynamic naming
#     filtered.to_csv(file_name, index=False) #save to csv   



# Save or inspect results
# df.to_csv('MASTER_FILE_COUNTY_CLUSTERS.csv', index=False)
# print(df[['County', 'Cluster']].head())
