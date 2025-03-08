import pandas as pd


#---------------------------------SUMMARIZE DATA BY STAT----------------------------------
# Read the column names from the first cluster file
# Convert them into a list
# Remove unnecessary columns ('Cluster', 'County', 'County_FIPS')
data_cols = list(pd.read_csv("cluster_1.csv").columns)
data_cols.remove('Cluster')
data_cols.remove('County')
data_cols.remove('County_FIPS')


# List of statistical measures to be computed
stats = ["mean", "median", "minVal", "maxVal", "stdev", "var", "quantile_25", "quantile_75"]

# Create a list to store cluster labels
clusters = []
for i in range(1,11):
    clusters.append(f"cluster_{i}")

# Dynamically create empty DataFrames for each statistical measure
# The index represents different clusters
for stat in stats:
    globals()[f"df_{stat}"] = pd.DataFrame(columns=data_cols, index=clusters)

# Initialize a nested dictionary to store computed values
# Example structure:
# all_stats = {"mean": {"Cluster 1": [], "Cluster 2": []}, "min": {"Cluster 1": [], "Cluster 2": []}}
all_stats = {stat: {} for stat in stats}

# Loop through each cluster (from 1 to 10)
for cluster in clusters:
    # Read the corresponding cluster data file
    data = pd.read_csv(f"clusters/{cluster}.csv")
    
    # Compute statistics for each column in the data file
    for col in data_cols:
        # Store the calculated statistics in the all_stats dictionary
        all_stats["mean"][cluster] = data[col].mean()
        all_stats["median"][cluster] = data[col].median()
        all_stats["minVal"][cluster] = data[col].min()
        all_stats["maxVal"][cluster] = data[col].max()
        all_stats["stdev"][cluster] = data[col].std()
        all_stats["var"][cluster] = data[col].var()
        all_stats["quantile_25"][cluster] = data[col].quantile(0.25)
        all_stats["quantile_75"][cluster] = data[col].quantile(0.75)

# Populate the DataFrames with the computed statistics
for stat in stats:
    for cluster in clusters:
        # Assign values from all_stats dictionary to the respective DataFrame
        globals()[f"df_{stat}"].loc[cluster, globals()[f"df_{stat}"].columns[:]] = all_stats[stat][cluster]
    
    # Save the DataFrame as a CSV file
    globals()[f"df_{stat}"].to_csv(f"data_by_stat/{stat}.csv", index=True)  
    
    
#---------------------------------SUMMARIZE DATA BY CLUSTER----------------------------------
for id in range(1,11):
    
    data = pd.read_csv(f"clusters/cluster_{id}.csv")
    data.dropna()
    metrics = data.columns.tolist()
    metrics.remove('County')
    metrics.remove('County_FIPS')
    metrics.remove('Cluster')
    print(metrics)
    
    sumStat = pd.DataFrame()
    sumStat['metrics']=metrics
    print(len(sumStat))
    
    mean = []
    median = []
    minVal = []
    maxVal = []
    stdev = []
    variance = []
    lower_quartile = []
    upper_quartile = []
    
    for metric in metrics:
        mean.append(data[metric].mean())
        median.append(data[metric].median())
        minVal.append(data[metric].min())
        maxVal.append(data[metric].max())
        stdev.append(data[metric].std())
        variance.append(data[metric].var())
        lower_quartile.append(data[metric].quantile(.25))
        upper_quartile.append(data[metric].quantile(.75))
        
    sumStat['mean']=mean
    sumStat['median']=median
    sumStat['min']=minVal
    sumStat['max']=maxVal
    sumStat['stdev']=stdev
    sumStat['variance']=variance
    sumStat['25th_perc']=lower_quartile
    sumStat['75th_perc']=upper_quartile
    
    print('mean',len(mean))
    print('median',len(median))
    print('min',len(minVal))
    print('max',len(maxVal))
    print('stdev',len(stdev))
    print('variance',len(variance))
    print('25th',len(lower_quartile))
    print('75th',len(upper_quartile))
    
    sumStat.to_csv(f'data_by_cluster/cluster{id}_sumStat.csv',index=False)

