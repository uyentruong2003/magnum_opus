import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


data = pd.read_csv(r"C:\Users\uyenk\OneDrive - The University of Alabama\Self-learning Programming\magnum_opus\MASTER_FILE_COUNTY_CLUSTERS.csv")
og_df = pd.DataFrame(data)


def min_max_scaling(metric,df):
    selectedData_df = df[[f"Tornado_{metric}",f"ThunderstormWind_{metric}",
                  f"Flood_{metric}",f"Hail_{metric}",
                  f"TropicalDepression_{metric}",f"TropicalStorm_{metric}",f"Hurricane_{metric}",
                  f"StormSurge/Tide_{metric}",f"CoastalFlood_{metric}","Cluster"]].copy()
    
    selectedData_df.fillna(0,inplace=True)
    # selectedData_df.columns = ["Tornado","ThunderstormWind",
    #               "Flood","Hail",
    #               "TropicalDepression","TropicalStorm","Hurricane",
    #               "StormSurge/Tide","CoastalFlood","Cluster"]
    
    # Calc agg means by cluster
    agg = selectedData_df.groupby('Cluster').mean()    
    # normalize agg means of clusters in range 0-1 by severe weather
    scaled_df = (agg - agg.min()) / (agg.max() - agg.min())
    scaled_df.fillna(0,inplace=True)
    print(scaled_df)
    return scaled_df


def plot_heatmap(metric,norm_df):
    #re-label col names
    norm_df.columns = ["Tornado","ThunderstormWind",
                  "Flood","Hail",
                  "TropicalDepression","TropicalStorm","Hurricane",
                  "StormSurge/Tide","CoastalFlood"]
    df = norm_df.transpose();
    plt.figure(figsize=(12, 6))
    
    sns.heatmap(
        df,
        annot=True,
        fmt=".2f",
        cmap="YlOrRd"
    )
    
    plt.title(f"Heatmap: Normalized Mean {metric} of Each Severe Weather Type Across Clusters",size=16, y=1.02, fontweight='bold')
    plt.xlabel("Cluster")
    plt.ylabel("Severe Weather Type")
    plt.tight_layout()
    plt.show()



def plot_radar_chart_all_clusters(norm_df, colors, metric):   
    #re-label col names
    norm_df.columns = ["Tornado","ThunderstormWind",
                  "Flood","Hail",
                  "TropicalDepression","TropicalStorm","Hurricane",
                  "StormSurge/Tide","CoastalFlood"]
    labels = norm_df.columns[0:]
    num_vars = len(labels)
    
    # Create angle values
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop
    
    num_clusters = len(norm_df)
    rows, cols = 2, 5  # Fixed layout: 2 rows x 5 columns
    
    # Create subplots
    fig, axs = plt.subplots(rows, cols, subplot_kw=dict(polar=True), figsize=(20,10))
    axs = axs.flatten()  # Flatten in case of 2D array

    for i in range(num_clusters):
        values = norm_df.iloc[i, 0:].tolist()
        values += values[:1]  # Complete the loop

        ax = axs[i]
        
        ax.plot(angles, values, color=colors[i], linewidth=1, linestyle='--', marker='o', markersize=4)
        ax.fill(angles, values, alpha=0.3, color=colors[i])  # Optional
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_yticklabels([])
        ax.set_title(f"Cluster {i+1}", size=10, y=1.1)
        
        
    fig.suptitle(f"Radar Charts: Dominant Severe Weather Types by {metric} of Each Cluster", size=27, y=1.02, fontweight='bold')
    plt.subplots_adjust(top=0.50)
    plt.tight_layout()
    plt.show()



colors = [
"#1f77b4",  # blue
"#ff7f0e",  # orange
"#2ca02c",  # green
"#d62728",  # red
"#9467bd",  # purple
"#8c564b",  # brown
"#e377c2",  # pink
"#7f7f7f",  # gray
"#bcbd22",  # yellow-green
"#17becf"   # cyan
]
# Plots by cluster mean counts
# plot_radar_chart_all_clusters(min_max_scaling("Count",og_df), colors,"Counts")
# plot_heatmap("Counts", min_max_scaling("Count",og_df))

def calc_impact_score(df):
    # min-max scaling the deaths, injuries, and propertyDamages of each severe weather type
    norm_deaths= min_max_scaling("Deaths", df)
    norm_injuries = min_max_scaling("Injuries",df)
    norm_propertyDamages = min_max_scaling("PropertyDamages",df)
    
    # merge 3 dfs into one
    norm_impact = pd.merge(norm_deaths, norm_injuries,on="Cluster")
    norm_impact = pd.merge(norm_impact, norm_propertyDamages,on="Cluster")
    
    weatherTypes = ["Tornado","ThunderstormWind",
                  "Flood","Hail",
                  "TropicalDepression","TropicalStorm","Hurricane",
                  "StormSurge/Tide","CoastalFlood"]
    
    # calc impact score for each severe weather type
    for w in weatherTypes:
        norm_impact[f"{w}_ImpactScore"] = (
        0.5 * norm_impact[f"{w}_Deaths"] +
        0.3 * norm_impact[f"{w}_Injuries"] +
        0.2 * norm_impact[f"{w}_PropertyDamages"]
        )
        #drop unnecessary cols after impact score calc is done
        norm_impact.drop([f"{w}_Deaths", f"{w}_Injuries", f"{w}_PropertyDamages"], axis=1, inplace=True)
    
    print(norm_impact)
    return norm_impact


# plot_heatmap("Impact Scores", calc_impact_score(og_df))
# plot_radar_chart_all_clusters(calc_impact_score(og_df), colors, "Impact Scores")

def boxplot_each_cluster(cluster, metric):
    cluster_data = pd.read_csv(rf"C:\Users\uyenk\OneDrive - The University of Alabama\Self-learning Programming\magnum_opus\clusters\cluster_{cluster}.csv")
    cluster_df = pd.DataFrame(cluster_data)
    
    data = {
        'County_FIPS': cluster_df["County_FIPS"],
        'Tornado': cluster_df[f"Tornado_{metric}"],
        'ThunderstormWind': cluster_df[f"ThunderstormWind_{metric}"],
        'CoastalFlood': cluster_df[f"CoastalFlood_{metric}"],
        'StormSurge/Tide': cluster_df[f"StormSurge/Tide_{metric}"],
        'Hurricane':cluster_df[f"Hurricane_{metric}"],
        'TropicalStorm':cluster_df[f"TropicalStorm_{metric}"],
        'TropicalDepression':cluster_df[f"TropicalDepression_{metric}"],
        'Flood':cluster_df[f"Flood_{metric}"],
        'Hail':cluster_df[f"Hail_{metric}"],
    }
    
    df = pd.DataFrame(data)
    
    # data_cols = ["Tornado","ThunderstormWind","CoastalFlood","StormSurge/Tide",
    #               "Hurricane","TropicalStorm","TropicalDepression","Flood","Hail"]    
    
    # Melt into long format
    df_long = df.melt(id_vars='County_FIPS', 
                      var_name='metric', 
                      value_name='value')
    df_long.fillna(0,inplace=True)
   
    # ==== Plot
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='metric', y='value', data=df_long)
    sns.stripplot(x='metric', y='value', data=df_long, 
              color='black', size=4, jitter=True)
    
   
    plt.xticks(rotation=45)
    plt.title(f"Cluster {cluster} Boxplot: Count of each Severe Weather Types")
    plt.tight_layout()
    plt.show()

 
    

for i in range(1,11):
    boxplot_each_cluster(f"{i}", "Count")