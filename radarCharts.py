import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# meanCountClusterData for 10 clusters

raw_data_df = pd.read_csv(r"C:\Users\uyenk\OneDrive - The University of Alabama\Self-learning Programming\magnum_opus\data_by_stat\mean.csv")
consolidated_df = raw_data_df[["Tornado_Count","ThunderstormWind_Count",
                               "StormSurge/Tide_Count","CoastalFlood_Count",
                               "Hurricane_Count","TropicalStorm_Count","TropicalDepression_Count",
                               "Flood_Count","Hail_Count"]]

consolidated_df.fillna(0, inplace=True)

#normalize data in range 0-1:
consolidated_df = (consolidated_df - consolidated_df.min()) / (consolidated_df.max() - consolidated_df.min())
consolidated_df = consolidated_df.copy()
consolidated_df["Cluster"]=[f'Cluster {i+1}' for i in range(10)]

def get_cluster_dict(index):
    return {
        'Cluster': [consolidated_df["Cluster"][index]],
        'Tornadoes': [consolidated_df["Tornado_Count"][index]],
        'Thunderstorm Winds': [consolidated_df["ThunderstormWind_Count"][index]],
        'Storm Tide/Surge': [consolidated_df["StormSurge/Tide_Count"][index]],
        'Coastal Flood': [consolidated_df["CoastalFlood_Count"][index]],
        'Hail': [consolidated_df["Hail_Count"][index]],
        'Flood': [consolidated_df["Flood_Count"][index]],
        'Tropical Depressions': [consolidated_df["TropicalDepression_Count"][index]],
        'Tropical Storms': [consolidated_df["TropicalStorm_Count"][index]],
        'Hurricane': [consolidated_df["Hurricane_Count"][index]]
    }

def get_all_clusters_dict():
    return{
    'Cluster': consolidated_df["Cluster"],
    'Tornadoes': consolidated_df["Tornado_Count"],
    'Thunderstorm Winds': consolidated_df["ThunderstormWind_Count"],
    'Storm Tide/Surge': consolidated_df["StormSurge/Tide_Count"],
    'Coastal Flood': consolidated_df["CoastalFlood_Count"],
    'Hail': consolidated_df["Hail_Count"],
    'Flood': consolidated_df["Flood_Count"],
    'Tropical Depressions': consolidated_df["TropicalDepression_Count"],
    'Tropical Storms': consolidated_df["TropicalStorm_Count"],
    'Hurricane': consolidated_df["Hurricane_Count"]
}


# Radar chart setup
def plot_all_clusters(df,colors):
    labels = df.columns[1:]
    num_vars = len(labels)
    
    
    # Create angle values
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop
    
    # Initialize plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # Plot each cluster
    for i in range(len(df)):
        values = df.iloc[i, 1:].tolist()
        values += values[:1]  # Complete the loop
        ax.plot(angles, values, label=df['Cluster'][i], color=colors[i], linewidth=2)
        ax.fill(angles, values, alpha=0.3, color=colors[i])
    
    # Add labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12)
    
    # Optional: set y-labels and limits
    ax.set_title("Radar Chart: Hazard Attributes per Cluster", size=16, y=1.1)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    
    plt.tight_layout()
    plt.savefig("plots/allClusters_radarCharts.png", bbox_inches='tight', dpi=300)
    plt.show()

def plot_one_cluster(df, color, save_path=None):
    labels = df.columns[1:]
    num_vars = len(labels)
    
    # Create angle values
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop
    
    # Initialize plot
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
    # Plot the cluster
    values = df.iloc[0, 1:].tolist()
    values += values[:1]
    ax.plot(angles, values, label=df['Cluster'][0], color=color, linewidth=2)
    ax.fill(angles, values, alpha=0.3, color=color)
    
    # Add category labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12)
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=10)
    
    # Add title and legend
    ax.set_title(f"Radar Chart - {df['Cluster'][0]}", size=16, y=1.1)
    ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
    
    plt.tight_layout()
    
    # Save the figure if a path is given
    if save_path:
        plt.savefig(save_path, bbox_inches='tight', dpi=300)
    
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
# Plot all the clusters
all_dfs = pd.DataFrame(get_all_clusters_dict())
plot_all_clusters(all_dfs, colors)

# Plot 1 cluster at a time
# for i in range(0,10):
#     single_df = pd.DataFrame(get_cluster_dict(i))
#     plot_one_cluster(single_df, colors[i], f"plots/Cluster{i+1}_radarChart.png")