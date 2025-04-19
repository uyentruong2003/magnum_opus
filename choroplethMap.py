import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# Load Alabama county shapefile
shapefile_path = r"C:\Users\uyenk\OneDrive - The University of Alabama\Self-learning Programming\magnum_opus\al_geo\tl_2021_01_cousub.shp"
gdf = gpd.read_file(shapefile_path)
print(gdf.columns)
print(gdf.head())
print(gdf[['COUNTYFP']])
gdf = gdf.dissolve(by='COUNTYFP')

# Load data
data_df = pd.read_csv(r"C:\Users\uyenk\OneDrive - The University of Alabama\Self-learning Programming\magnum_opus\MASTER_FILE_COUNTY_CLUSTERS.csv")
print(data_df.columns)

# Dissolve subdivisions into counties



# # Ensure County_FIPS is treated as a string
# data_df = data_df.rename(columns={'County_FIPS': 'COUNTYFP'})
# data_df['COUNTYFP'] = data_df['COUNTYFP'].astype(str)

# # Loop through rows to format County_FIPS
# for index, row in data_df.iterrows():
#     curr_FIP = row['COUNTYFP']  # Get the current FIPS as a string

#     # Add leading zeros if needed
#     if len(curr_FIP) == 1:
#         data_df.at[index, 'COUNTYFP'] = "00" + curr_FIP
#     elif len(curr_FIP) == 2:
#         data_df.at[index, 'COUNTYFP'] = "0" + curr_FIP

def transformCountyFIPS(df):
    # Ensure County_FIPS is treated as a string
    df = df.rename(columns={'County_FIPS': 'COUNTYFP'})
    df['COUNTYFP'] = df['COUNTYFP'].astype(str)
    
    # Loop through rows to format County_FIPS
    for index, row in df.iterrows():
        curr_FIP = row['COUNTYFP']  # Get the current FIPS as a string
    
        # Add leading zeros if needed
        if len(curr_FIP) == 1:
            df.at[index, 'COUNTYFP'] = "00" + curr_FIP
        elif len(curr_FIP) == 2:
            df.at[index, 'COUNTYFP'] = "0" + curr_FIP
    return df

# this function plots the data by county. If you want to plot by cluster, mapStyling="tab10"        
def plotDataByCounty(data_col,mapStyling):
    filtered_df = data_df[['County', 'COUNTYFP',data_col]]
    filtered_df.head()

    # Merge data:
    plot_gdf = gdf.merge(filtered_df, on="COUNTYFP", how="left").fillna(0)
    
    # Custom color if plot map by clusters
    # customColors = ["red", "blue", "magenta", "lime", "green",
    #       "orange", "purple", "yellow", "cyan", "brown"]
    
    tab10_colors = [
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
    
    # Plot the map
    fig, ax = plt.subplots(1, 1, figsize=(10, 8))
    if data_col == "Cluster":
        plot_gdf.plot(column=data_col, cmap=ListedColormap(tab10_colors), linewidth=0.8, edgecolor="black", legend=True, ax=ax)
    else:
        plot_gdf.plot(column=data_col, cmap=mapStyling, linewidth=0.8, edgecolor="black", legend=True, ax=ax)
    ax.set_title(f"{data_col} by county")
    plt.axis("off")
    plt.show()


# # plot data metrics by county
data_df = transformCountyFIPS(data_df)



plotDataByCounty("Tornado_Count","YlOrBr")
# plotDataByCounty("Cluster", "tab10")



