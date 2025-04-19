import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Create heatmap--------------
data = pd.read_csv(r"C:\Users\uyenk\OneDrive - The University of Alabama\Self-learning Programming\magnum_opus\MASTER_FILE_COUNTY_CLUSTERS.csv")
df = pd.DataFrame(data)


def norm_agg_mean_data(metric):
    selectedData_df = df[[f"Tornado_{metric}",f"ThunderstormWind_{metric}",
                 f"StormSurge/Tide_{metric}",f"CoastalFlood_{metric}",
                 f"Hurricane_{metric}",f"TropicalStorm_{metric}",f"TropicalDepression_{metric}",
                 f"Flood_{metric}",f"Hail_{metric}","Cluster"]]
    selectedData_df.fillna(0,inplace=True)
    selectedData_df.columns = ["Tornado","ThunderstormWind",
                 "StormSurge/Tide","CoastalFlood",
                 "Hurricane","TropicalStorm","TropicalDepression",
                 "Flood","Hail","Cluster"]
    
    # Calc agg mean by cluster
    agg = selectedData_df.groupby('Cluster').mean()    
    # normalize agg means of clusters in range 0-1 by severe weather
    normalized_df = (agg - agg.min()) / (agg.max() - agg.min())
    normalized_df = normalized_df.transpose();
    normalized_df.fillna(0,inplace=True)
    print(normalized_df)
    return normalized_df


def plot_heatmap(metric,df):
    plt.figure(figsize=(12, 6))
    
    sns.heatmap(
        df,
        annot=True,
        fmt=".2f",
        cmap="YlOrRd"
    )
    
    plt.title(f"Heatmap: Normalized Average {metric} of Each Severe Weather Across Clusters")
    plt.xlabel("Cluster")
    plt.ylabel("Severe Weather Type")
    plt.tight_layout()
    plt.show()

def plot_radar_chart(metric, df):
    # Setup
    labels = df.columns.astype(str)  # Cluster numbers
    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    angles += angles[:1]  # close the loop
    
    # Create radar charts
    fig, axs = plt.subplots(3, 3, subplot_kw={'projection': 'polar'}, figsize=(15, 12))
    axs = axs.flatten()
    
    for i, (weather_type, row) in enumerate(df.iterrows()):
        values = row.tolist()
        values += values[:1]  # close the loop
        ax = axs[i]
        ax.plot(angles, values, linewidth=2, label=weather_type)
        ax.fill(angles, values, alpha=0.25)
        ax.set_title(weather_type, size=12)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels)
        ax.set_yticklabels([])
    
    plt.tight_layout()
    plt.suptitle(f"Radar Charts: Severe Weather Prevalence Across Clusters", fontsize=16, y=1.02)
    plt.show()



# plot_heatmap("Count", norm_agg_mean_data("Count"))

plot_radar_chart("Count", norm_agg_mean_data("Count"))
# norm_agg_mean_data("Deaths")
# norm_agg_mean_data("Injuries")
# norm_agg_mean_data("PropertyDamages")