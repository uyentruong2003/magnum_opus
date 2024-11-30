import pandas as pd
import numpy as np

cyclones = pd.read_csv("TROPICAL_DEPRESSIONS_STORMS_AND_HURRICANES_2000_2024_ALL.csv")
dfCyclones = pd.DataFrame(cyclones).drop_duplicates()

winds = pd.read_csv("TORNADOES_AND_THUNDERSTORM_WINDS_2000_2024_ALL.csv")
dfWinds = pd.DataFrame(winds).drop_duplicates()

seaLevels = pd.read_csv("COASTAL_FLOODS_AND_STORM_SURGE.csv")
dfSeaLevels = pd.DataFrame(seaLevels).drop_duplicates()

precip = pd.read_csv("HAIL_AND_FLOOD_2000_2024.csv")
dfPrecip = pd.DataFrame(precip).drop_duplicates()


#This is a function to construct an aggregate table for count of events, # of deaths, injuries, and property damages
def createAggregateTable(df_raw_data, event_type_list,loc_type,FIPS_type):
    dfAggregate = pd.DataFrame()
    dfAggregate[FIPS_type] = df_raw_data['CZ_FIPS']
    dfAggregate[loc_type] = df_raw_data['CZ_NAME_STR']
    dfAggregate.drop_duplicates(inplace=True)
    metrics = {
        "Count": lambda df, row, event: len(df[(df["CZ_FIPS"] == row[FIPS_type]) & (df["EVENT_TYPE"] == event)]),
        "Deaths": lambda df, row, event: df[(df["CZ_FIPS"] == row[FIPS_type]) & (df["EVENT_TYPE"] == event)]['DEATHS_DIRECT'].sum(),
        "Injuries": lambda df, row, event: df[(df["CZ_FIPS"] == row[FIPS_type]) & (df["EVENT_TYPE"] == event)]['INJURIES_DIRECT'].sum(),
        "PropertyDamages": lambda df, row, event: df[(df["CZ_FIPS"] == row[FIPS_type]) & (df["EVENT_TYPE"] == event)]['DAMAGE_PROPERTY_NUM'].sum(),
    }

    # Initialize empty dictionaries to store results for each metric
    results = {metric: {event: [] for event in event_type_list} for metric in metrics.keys()}

    # Iterate over each row in dfAggregate
    for _, row in dfAggregate.iterrows():
        for event in event_type_list:
            for metric, func in metrics.items():
                results[metric][event].append(func(df_raw_data, row, event))

    # Add results to dfAggregate
    for metric, event_data in results.items():
        for event, values in event_data.items():
            column_name = f"{event.replace(' ', '')}_{metric}"
            dfAggregate[column_name] = values

    return dfAggregate


# CYCLONES (zone):
cyclone_event_types = ["Hurricane", "Tropical Storm", "Tropical Depression"]
dfCyclonesAggregate = createAggregateTable(dfCyclones,cyclone_event_types,"Zone","Zone_FIPS")
# print(dfCyclonesAggregate.columns)


# WINDS (county):
wind_event_types = ["Tornado", "Thunderstorm Wind"]
dfWindsAggregate= createAggregateTable(dfWinds, wind_event_types,"County","County_FIPS")
# print(dfWindsAggregate.columns)
#Including Magnitudes (EF scale for tornadoes, and knotts or Beaufort scale for thunderstorm winds)

# PRECIPITATION (county):
precip_event_types = ["Hails","Flood"]
dfPrecipAggregate = createAggregateTable(dfPrecip,precip_event_types,"County","County_FIPS")
#Including Magnitudes for Hails (inches)
# print(dfPrecipAggregate)

# SEA LEVELS (zone):
seaLevel_event_types = ["Coastal Flood","Storm Surge/Tide"]
dfSeaLevelsAggregate= createAggregateTable(dfSeaLevels, seaLevel_event_types,"Zone","Zone_FIPS")
# print(dfSeaLevelsAggregate)

# ZONE TO COUNTY CONVERSION
counties = pd.read_excel("county_zone_correl.xlsx")
dfCounties = pd.DataFrame(counties)
# print(dfCounties.columns)
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
dfSeaLevelsAggregate = ConvertZoneToCounty(dfSeaLevelsAggregate)
dfCyclonesAggregate = ConvertZoneToCounty(dfCyclonesAggregate)

# Create a dfCounty with 67 AL counties based on the zone_county_correl df
dfCounty = dfZoneCounty.drop("ZONE",axis=1).rename(columns = {"COUNTY":"County"}).drop_duplicates()
dfCounty.sort_values(by="County",ascending=True,inplace=True)
dfCounty.reset_index(drop=True, inplace=True)
# print(dfCounty)

# Create the master dataset that combines all the severe weather data by county

# # Check dtype of all 3 datasets
# print("dfWinds\n",dfWindsAggregate.dtypes)
# print("\ndfSeaLevels\n",dfSeaLevelsAggregate.dtypes)
# print("\ndfCyclones\n",dfCyclonesAggregate.dtypes)
# print("\ndfPrecip\n",dfPrecipAggregate.dtypes)

dfWindsAggregate["County_FIPS"] = dfWindsAggregate["County_FIPS"].astype(str) #County_FIPS of all datasets must be the same dtype: str
dfPrecipAggregate["County_FIPS"] = dfPrecipAggregate["County_FIPS"].astype(str) #County_FIPS of all datasets must be the same dtype: str
dfMaster = pd.merge(dfCounty,dfWindsAggregate.drop('County',axis=1),on="County_FIPS",how="left") # merge winds into master df
dfMaster = pd.merge(dfMaster,dfSeaLevelsAggregate.drop('County',axis=1),on="County_FIPS",how="left") # merge sea levels into master df
dfMaster = pd.merge(dfMaster,dfCyclonesAggregate.drop('County',axis=1),on="County_FIPS",how="left") # merge cyclones into master df
dfMaster = pd.merge(dfMaster,dfPrecipAggregate.drop('County',axis=1),on="County_FIPS",how="left") # merge precip into master df

# pd.set_option('display.max_rows', None)
# print(dfMaster.columns)
# print(dfMaster)
# pd.reset_option('display.max_rows')