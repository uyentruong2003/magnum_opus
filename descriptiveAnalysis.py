import pandas as pd
import os

#---------------------------------SUMMARIZE DATA BY STAT----------------------------------
# Get column names from the first cluster file
data_cols = list(pd.read_csv("clusters/cluster_1.csv").columns)
data_cols.remove('Cluster')
data_cols.remove('County')
data_cols.remove('County_FIPS')

# List of statistical measures to be computed
stats = ["mean", "median", "minVal", "maxVal", "stdev", "var", "quantile_25", "quantile_75"]

# Create a list of cluster labels
clusters = [f"cluster_{i}" for i in range(1, 11)]

# Initialize a nested dictionary to store computed statistics
all_stats = {stat: {cluster: {} for cluster in clusters} for stat in stats}
# {stat : {cluster : {col : value}}}
# Example: all_stats = 
    #{"mean":
        #{"cluster_1":{"ThunderstormWind_Count":11.11, "Tornado_Count":25.0, ...},
        #{"cluster_2":{"ThunderstormWind_Count":5.8, "Tornado_Count":12.5,...},
        # ...
    #},
    #{"median":
        #{"cluster_1":{"ThunderstormWind_Count":11.11, "Tornado_Count":25.0,...},
        #{"cluster_2":{"ThunderstormWind_Count":5.8, "Tornado_Count":12.5},...,
    #},
    #...}

# Loop through each cluster
for cluster in clusters:
    data = pd.read_csv(f"clusters/{cluster}.csv")

    # Compute statistics for each column
    for col in data_cols:

        all_stats["mean"][cluster][col] = data[col].mean()
        all_stats["median"][cluster][col] = data[col].median()
        all_stats["minVal"][cluster][col] = data[col].min()
        all_stats["maxVal"][cluster][col] = data[col].max()
        all_stats["stdev"][cluster][col] = data[col].std()
        all_stats["var"][cluster][col] = data[col].var()
        all_stats["quantile_25"][cluster][col] = data[col].quantile(0.25)
        all_stats["quantile_75"][cluster][col] = data[col].quantile(0.75)

# Create DataFrames and save to CSV
all_stats_csv = []
for stat in stats:
    # Create DataFrames
    df_stat = pd.DataFrame.from_dict(all_stats[stat], orient="index")
    all_stats_csv.append(f"data_by_stat/{stat}.csv")
    
    # Save to separate CSV
    # df_stat.to_csv(f"data_by_stat/{stat}.csv", index=True)
    
# Compile all stats into multiple sheets of the same Excel workbook

with pd.ExcelWriter('data_by_stat/ALL_STATS.xlsx', engine='openpyxl') as writer:
    for csv_file in all_stats_csv:
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)
        
        # Use the file name (without extension) as the sheet name
        sheet_name = os.path.splitext(os.path.basename(csv_file))[0]
        
        # Write the DataFrame to the specified sheet
        df.to_excel(writer, sheet_name=sheet_name, index=False)

    
#---------------------------------SUMMARIZE DATA BY CLUSTER----------------------------------
# for id in range(1,11):
    
#     data = pd.read_csv(f"clusters/cluster_{id}.csv")
#     data.dropna()
#     data_cols = data.columns.tolist()
#     data_cols.remove('County')
#     data_cols.remove('County_FIPS')
#     data_cols.remove('Cluster')
#     print(data_cols)
    
#     sumStat = pd.DataFrame()
#     sumStat['data_cols']=data_cols
#     print(len(sumStat))
    
#     mean = []
#     median = []
#     minVal = []
#     maxVal = []
#     stdev = []
#     variance = []
#     lower_quartile = []
#     upper_quartile = []
    
#     for col in data_cols:
#         mean.append(data[col].mean())
#         median.append(data[col].median())
#         minVal.append(data[col].min())
#         maxVal.append(data[col].max())
#         stdev.append(data[col].std())
#         variance.append(data[col].var())
#         lower_quartile.append(data[col].quantile(.25))
#         upper_quartile.append(data[col].quantile(.75))
        
#     sumStat['mean']=mean
#     sumStat['median']=median
#     sumStat['min']=minVal
#     sumStat['max']=maxVal
#     sumStat['stdev']=stdev
#     sumStat['variance']=variance
#     sumStat['25th_perc']=lower_quartile
#     sumStat['75th_perc']=upper_quartile
    
#     print('mean',len(mean))
#     print('median',len(median))
#     print('min',len(minVal))
#     print('max',len(maxVal))
#     print('stdev',len(stdev))
#     print('variance',len(variance))
#     print('25th',len(lower_quartile))
#     print('75th',len(upper_quartile))
    
    # sumStat.to_csv(f'data_by_cluster/cluster{id}_sumStat.csv',index=False)

