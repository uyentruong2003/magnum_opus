import pandas as pd
import numpy as np

cyclones = pd.read_csv("TROPICAL_DEPRESSIONS_STORMS_AND_HURRICANES_2000_2024_ALL.csv")
dfCyclones = pd.DataFrame(cyclones)
dfCyclones.drop_duplicates()

winds = pd.read_csv("TORNADOES_AND_THUNDERSTORM_WINDS_2000_2024_ALL.csv")
dfWinds = pd.DataFrame(winds)
dfWinds.drop_duplicates()

seaLevels = pd.read_csv("COASTAL_FLOODS_AND_STORM_SURGE.csv")
dfSeaLevels = pd.DataFrame(seaLevels)
dfSeaLevels.drop_duplicates()


#This is a function to construct a summary table for count of events, # of deaths, injuries, and property damages
def createSummaryTable(df_raw_data, event_type_list,loc_type,FIPS_type):
    dfSummary = pd.DataFrame()
    dfSummary[FIPS_type] = df_raw_data['CZ_FIPS']
    dfSummary[loc_type] = df_raw_data['CZ_NAME_STR']
    dfSummary.drop_duplicates(inplace=True)
    metrics = {
        "Count": lambda df, row, event: len(df[(df["CZ_FIPS"] == row[FIPS_type]) & (df["EVENT_TYPE"] == event)]),
        "Deaths": lambda df, row, event: df[(df["CZ_FIPS"] == row[FIPS_type]) & (df["EVENT_TYPE"] == event)]['DEATHS_DIRECT'].sum(),
        "Injuries": lambda df, row, event: df[(df["CZ_FIPS"] == row[FIPS_type]) & (df["EVENT_TYPE"] == event)]['INJURIES_DIRECT'].sum(),
        "PropertyDamages": lambda df, row, event: df[(df["CZ_FIPS"] == row[FIPS_type]) & (df["EVENT_TYPE"] == event)]['DAMAGE_PROPERTY_NUM'].sum(),
    }

    # Initialize empty dictionaries to store results for each metric
    results = {metric: {event: [] for event in event_type_list} for metric in metrics.keys()}

    # Iterate over each row in dfSummary
    for _, row in dfSummary.iterrows():
        for event in event_type_list:
            for metric, func in metrics.items():
                results[metric][event].append(func(df_raw_data, row, event))

    # Add results to dfSummary
    for metric, event_data in results.items():
        for event, values in event_data.items():
            column_name = f"{event.replace(' ', '')}_{metric}"
            dfSummary[column_name] = values

    return dfSummary


# CYCLONES (zone):
cyclone_event_types = ["Hurricane", "Tropical Storm", "Tropical Depression"]
dfCyclonesSummary = createSummaryTable(dfCyclones,cyclone_event_types,"Zone","Zone_FIPS")
# print(dfCyclonesSummary.columns)


# WINDS (county):
wind_event_types = ["Tornado", "Thunderstorm Wind"]
dfWindsSummary= createSummaryTable(dfWinds, wind_event_types,"County","County_FIPS")
# print(dfWindsSummary.columns)
#Including Magnitudes (EF scale for tornadoes, and knotts or Beaufort scale for thunderstorm winds)

# HAIL (zone):
#Including Magnitudes (inches)

# FLOOD (county):

# SEA LEVELS (zone):
seaLevel_event_types = ["Coastal Flood","Storm Surge/Tide"]
dfSeaLevelsSummary= createSummaryTable(dfSeaLevels, seaLevel_event_types,"Zone","Zone_FIPS")
# print(dfSeaLevelsSummary)

# ZONE TO COUNTY CONVERSION
counties = pd.read_excel("county_zone_correl.xlsx")
dfCounties = pd.DataFrame(counties)
print(dfCounties.columns)
dfZoneCounty = dfCounties[dfCounties['STATE']=='AL'][['ZONE','FIPS','COUNTY']]
dfZoneCounty = dfZoneCounty.reset_index(drop=True)

# get the county part of the full FIPS codes (5-digit FIPS code, first 2 are state fips, last 3 are county fips):
county_FIPS = []
for _, row in dfZoneCounty.iterrows():
    county_FIPS.append(str(row["FIPS"])[-3:].lstrip('0'))

dfZoneCounty['County_FIPS'] = county_FIPS
dfZoneCounty = dfZoneCounty.drop('FIPS',axis=1)

# Function to vlookup the corresponding county of the zone (for datasets categorized by zone instead of county)
def ConvertZoneToCounty (df):
    df = pd.merge(df, dfZoneCounty[["ZONE","County_FIPS","COUNTY"]], left_on='Zone_FIPS', right_on='ZONE', how='left').drop(['ZONE','Zone','Zone_FIPS'],axis=1)
    df = df.rename(columns={"COUNTY":"County"})
    return df

# transform zone-based dfs to county-based dfs
dfSeaLevelsSummary = ConvertZoneToCounty(dfSeaLevelsSummary)
dfCyclonesSummary = ConvertZoneToCounty(dfCyclonesSummary)

# Create a dfCounty with 67 AL counties based on the zone_county_correl df
dfCounty = dfZoneCounty.drop("ZONE",axis=1).rename(columns = {"COUNTY":"County"}).drop_duplicates()
dfCounty.sort_values(by="County",ascending=True,inplace=True)
dfCounty.reset_index(drop=True, inplace=True)
print(dfCounty)

# Create the master dataset that combines all the severe weather data by county

# # Check dtype of all 3 datasets
# print("dfWinds\n",dfWindsSummary.dtypes)
# print("\ndfSeaLevels\n",dfSeaLevelsSummary.dtypes)
# print("\ndfCyclones\n",dfCyclonesSummary.dtypes)

dfWindsSummary["County_FIPS"] = dfWindsSummary["County_FIPS"].astype(str) #County_FIPS of both datasets must be the same dtype: str
dfMaster = pd.merge(dfCounty,dfWindsSummary.drop('County',axis=1),on="County_FIPS",how="left") # merge winds into master df
dfMaster = pd.merge(dfMaster,dfSeaLevelsSummary.drop('County',axis=1),on="County_FIPS",how="left") # merge sea levels into master df
dfMaster = pd.merge(dfMaster,dfCyclonesSummary.drop('County',axis=1),on="County_FIPS",how="left") # merge cyclones into master df

pd.set_option('display.max_rows', None)
print(dfMaster.columns)
print(dfMaster)
pd.reset_option('display.max_rows')