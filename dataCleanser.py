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
def createAggregateTable(df_raw_data,loc_type,FIPS_type):
     # Group by FIPS code and location
    grouped = df_raw_data.groupby(["CZ_FIPS", "CZ_NAME_STR", "EVENT_TYPE"]).agg(
        Count=("EVENT_TYPE", "size"),
        Deaths=("DEATHS_DIRECT", "sum"),
        Injuries=("INJURIES_DIRECT", "sum"),
        PropertyDamages=("DAMAGE_PROPERTY_NUM", "sum"),
    ).reset_index()

    # Pivot the table to create separate columns for each event type and metric
    pivoted = grouped.pivot(
        index=["CZ_FIPS", "CZ_NAME_STR"],
        columns="EVENT_TYPE",
        values=["Count", "Deaths", "Injuries", "PropertyDamages"]
    )
    
    # Flatten the MultiIndex columns
    pivoted.columns = [
        f"{event.replace(' ', '')}_{metric}" for metric, event in pivoted.columns
    ]
    
    # Reset index to return a clean DataFrame
    dfAggregate = pivoted.reset_index()

    # Rename columns
    dfAggregate = dfAggregate.rename(columns = {"CZ_FIPS": FIPS_type, "CZ_NAME_STR":loc_type})

    return dfAggregate


# CYCLONES (zone):
dfCyclonesAggregate = createAggregateTable(dfCyclones,"Zone","Zone_FIPS")
# print(dfCyclonesAggregate.columns)


# WINDS (county):
dfWindsAggregate= createAggregateTable(dfWinds,"County","County_FIPS")
# print(dfWindsAggregate.columns)
#Including Magnitudes (EF scale for tornadoes, and knotts or Beaufort scale for thunderstorm winds)

# SEVERE PRECIPITATION (county):
dfPrecipAggregate = createAggregateTable(dfPrecip,"County","County_FIPS")
#Including Magnitudes for Hails (inches)
# print(dfPrecipAggregate)

# SEA LEVELS AKA COASTAL INUNDATION (zone):
dfSeaLevelsAggregate= createAggregateTable(dfSeaLevels,"Zone","Zone_FIPS")
# print(dfSeaLevelsAggregate)

# ZONE TO COUNTY CONVERSION
cz = pd.read_excel("county_zone_correl.xlsx")
dfCZ = pd.DataFrame(cz)
# print(dfCZ.columns)
dfZoneCounty = dfCZ[dfCZ['STATE']=='AL'][['ZONE','FIPS','COUNTY']]
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

# AGGREGATE MAGNITUDE/ EF SCALES--------------------------------------------------------------------------------------------------
# # If these tests below result in empty dataframe, it's confirmed that:
# # ...all thunderstorm winds has a magnitude
# print(dfWinds[dfWinds["MAGNITUDE"].isna() & dfWinds["EVENT_TYPE"]=="Thunderstorm Wind"][["CZ_NAME_STR","EVENT_TYPE", "MAGNITUDE"]])
# # ...none of the tornadoes has a magnitude
# print(dfWinds[dfWinds["MAGNITUDE"].notna() & dfWinds["EVENT_TYPE"]=="Tornado"][["CZ_NAME_STR","EVENT_TYPE","MAGNITUDE"]])
# # ...all tornadoes have an F/EF scale
# print(dfWinds[dfWinds["TOR_F_SCALE"].isna() & dfWinds["EVENT_TYPE"]=="Tornado"][["CZ_NAME_STR", "EVENT_TYPE","TOR_F_SCALE"]])
# # ...all hails has a magnitude
# print(dfPrecip[dfPrecip["MAGNITUDE"].isna() & dfPrecip["EVENT_TYPE"]=="Hail"][["CZ_NAME_STR", "EVENT_TYPE","MAGNITUDE"]])


dfTornadoMagnitude = dfWinds[dfWinds["EVENT_TYPE"]=="Tornado"][["CZ_NAME_STR","CZ_FIPS","EVENT_TYPE","TOR_F_SCALE"]].rename(columns={"CZ_NAME_STR":"County","CZ_FIPS":"County_FIPS"}) #tornado F scales
dfThunderstormWindMagnitude = dfWinds[dfWinds["EVENT_TYPE"]=="Thunderstorm Wind"][["CZ_NAME_STR","CZ_FIPS","EVENT_TYPE","MAGNITUDE"]].rename(columns={"CZ_NAME_STR":"County","CZ_FIPS":"County_FIPS"}) # thunderstorm wind magnitude (in knotts)
dfHailMagnitude = dfPrecip[dfPrecip["EVENT_TYPE"]=="Hail"][["CZ_NAME_STR","CZ_FIPS","EVENT_TYPE","MAGNITUDE"]].rename(columns={"CZ_NAME_STR":"County","CZ_FIPS":"County_FIPS"}) # hail magnitude (in inches)

dfTornadoMagnitude["MAGNITUDE"] = dfTornadoMagnitude["TOR_F_SCALE"].str[-1:] 
dfTornadoMagnitude.loc[dfTornadoMagnitude["MAGNITUDE"] == "U", "MAGNITUDE"] = 0 #replace U from EFU (EF unknown) to 0
dfTornadoMagnitude["MAGNITUDE"] = dfTornadoMagnitude["MAGNITUDE"].astype(float)
dfThunderstormWindMagnitude["MAGNITUDE"] = dfThunderstormWindMagnitude["MAGNITUDE"].astype(float)
dfHailMagnitude["MAGNITUDE"] = dfHailMagnitude["MAGNITUDE"].astype(float)

print(dfCounty)

def createAggregateTable(df_raw_data):
    dfAverageMagnitude = (
        df_raw_data.groupby(["County_FIPS", "County"], as_index=False)
        .agg(AverageMagnitude=("MAGNITUDE", "mean"))
    )
    return dfAverageMagnitude

print(createAggregateTable(dfTornadoMagnitude))
