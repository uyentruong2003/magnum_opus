import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# meanCountClusterData for 10 clusters

raw_data_df = pd.read_csv(r"C:\Users\uyenk\OneDrive - The University of Alabama\Self-learning Programming\magnum_opus\data_by_stat\mean.csv")
consolidated_df = raw_data_df[["Tornado_Count","ThunderstormWind_Count",
                               "StormSurge/Tide_Count","CoastalFlood_Count",
                               "Hurricane_Count","TropicalStorm_Count","TropicalDepression_Count",
                               "Flood_Count","Hail_Count"]]

consolidated_df.fillna(0, inplace=True)

#normalization: cluster data is scaled in range 0-1 by weather type
normalized_df = (consolidated_df - consolidated_df.min()) / (consolidated_df.max() - consolidated_df.min())
normalized_df = normalized_df.copy()
normalized_df["Cluster"]=[f'Cluster {i+1}' for i in range(10)]

def get_cluster_dict(index):
    return {
        'Cluster': [normalized_df["Cluster"][index]],
        'Tornadoes': [normalized_df["Tornado_Count"][index]],
        'Thunderstorm Winds': [normalized_df["ThunderstormWind_Count"][index]],
        'Storm Tide/Surge': [normalized_df["StormSurge/Tide_Count"][index]],
        'Coastal Flood': [normalized_df["CoastalFlood_Count"][index]],
        'Hail': [normalized_df["Hail_Count"][index]],
        'Flood': [normalized_df["Flood_Count"][index]],
        'Tropical Depressions': [normalized_df["TropicalDepression_Count"][index]],
        'Tropical Storms': [normalized_df["TropicalStorm_Count"][index]],
        'Hurricane': [normalized_df["Hurricane_Count"][index]]
    }

def get_all_clusters_dict():
    return{
    'Cluster': normalized_df["Cluster"],
    'Tornadoes': normalized_df["Tornado_Count"],
    'Thunderstorm Winds': normalized_df["ThunderstormWind_Count"],
    'Storm Tide/Surge': normalized_df["StormSurge/Tide_Count"],
    'Coastal Flood': normalized_df["CoastalFlood_Count"],
    'Hail': normalized_df["Hail_Count"],
    'Flood': normalized_df["Flood_Count"],
    'Tropical Depressions': normalized_df["TropicalDepression_Count"],
    'Tropical Storms': normalized_df["TropicalStorm_Count"],
    'Hurricane': normalized_df["Hurricane_Count"]
}


# Radar chart setup
def plot_all_clusters(df, colors):
    labels = df.columns[1:]
    num_vars = len(labels)
    
    # Create angle values
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]  # Complete the loop
    
    num_clusters = len(df)
    rows, cols = 2, 5  # Fixed layout: 2 rows x 5 columns
    
    # Create subplots
    fig, axs = plt.subplots(rows, cols, subplot_kw=dict(polar=True), figsize=(20, 10))
    axs = axs.flatten()  # Flatten in case of 2D array

    for i in range(num_clusters):
        values = df.iloc[i, 1:].tolist()
        values += values[:1]  # Complete the loop

        ax = axs[i]
        
        ax.plot(angles, values, color=colors[i], linewidth=1, linestyle='--', marker='o', markersize=4)
        ax.fill(angles, values, alpha=0.3, color=colors[i])  # Optional
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_title(f"Cluster {df['Cluster'][i]}", size=10, y=1.1)

    # Hide any unused subplots (just in case)
    for j in range(num_clusters, len(axs)):
        fig.delaxes(axs[j])
    
    fig.suptitle("Radar Charts by Cluster\nNormalized Average Count of Severe Weather Types", size=16, y=1.02)
    plt.tight_layout()
    # plt.subplots_adjust(top=0.95)  # Adjust spacing to make room for the main title
    plt.savefig("plots/allClusters_radarCharts.png", bbox_inches='tight', dpi=300)
    plt.show()

# def plot_one_cluster(df, color, save_path=None):
#     labels = df.columns[1:]
#     num_vars = len(labels)
    
#     # Create angle values
#     angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()
#     angles += angles[:1]  # Complete the loop
    
#     # Initialize plot
#     fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    
#     # Plot the cluster
#     values = df.iloc[0, 1:].tolist()
#     values += values[:1]
#     ax.plot(angles, values, label=df['Cluster'][0], color=color, linewidth=2)
#     ax.fill(angles, values, alpha=0.3, color=color)
    
#     # Add category labels
#     ax.set_xticks(angles[:-1])
#     ax.set_xticklabels(labels, fontsize=12)
#     ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
#     ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=10)
    
#     # Add title and legend
#     ax.set_title(f"Radar Chart - {df['Cluster'][0]}", size=16, y=1.1)
#     ax.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
    
#     plt.tight_layout()
    
    # Save the figure if a path is given
    # if save_path:
    #     plt.savefig(save_path, bbox_inches='tight', dpi=300)
    
    # plt.show()

# def plot_radar_chart(metric, df):
    # # Setup
    # labels = df.columns.astype(str)  # Cluster numbers
    # angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
    # angles += angles[:1]  # close the loop
    
    # # Create radar charts
    # fig, axs = plt.subplots(2, 5, subplot_kw=dict(polar=True), figsize=(20, 10))
    # axs = axs.flatten()
    
    # for i, (weather_type, row) in enumerate(df.iterrows()):
    #     values = row.tolist()
    #     values += values[:1]  # close the loop
    #     ax = axs[i]
    #     ax.plot(angles, values, linewidth=2, label=weather_type)
    #     ax.fill(angles, values, alpha=0.25)
    #     ax.set_title(weather_type, size=12)
    #     ax.set_xticks(angles[:-1])
    #     ax.set_xticklabels(labels)
    #     ax.set_yticklabels([])
    
    # plt.tight_layout()
    # plt.suptitle(f"Radar Charts: Severe Weather Prevalence Across Clusters", fontsize=16, y=1.02)
    # plt.show()

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
print(all_dfs)
plot_all_clusters(all_dfs, colors)

# Plot 1 cluster at a time
# for i in range(0,10):
#     single_df = pd.DataFrame(get_cluster_dict(i))
#     plot_one_cluster(single_df, colors[i], f"plots/Cluster{i+1}_radarChart.png")

