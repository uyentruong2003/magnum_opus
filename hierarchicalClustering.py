print("Hello World!")
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
import matplotlib.pyplot as plt
import seaborn as sns


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

# loop thru the unique_ids and filter df by cluster.
# Save counties to csv by cluster
for id in cluster_ids:
    filtered = df[df['Cluster'] == id] #filter by cluster
    file_name = f"clusters/cluster_{id}.csv" #dynamic naming
    filtered.to_csv(file_name, index=False) #save to csv   


# Plot Cluster Map
# Create a DataFrame for the heatmap with counties as row labels
# clustered_df = pd.DataFrame(scaled_data, index=df['County'], columns=cols_pre_clustering)

# # Plot using seaborn's clustermap
# sns.clustermap(
#     clustered_df,
#     method='ward',  # Linkage method
#     metric='euclidean',  # Distance metric
#     figsize=(12, 10),
#     cmap='viridis',  # Color map
#     standard_scale=1,  # Normalize data (columns)
#     row_cluster=True,  # Enable row clustering
#     col_cluster=False  # Disable column clustering to focus on counties
# )

# plt.title('Cluster Map of Alabama Counties')
# plt.show()



# # Save or inspect results
# df.to_csv('clustered_counties.csv', index=False)
# print(df[['County', 'Cluster']].head())
