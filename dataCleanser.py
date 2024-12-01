import pandas as pd
import numpy as np
# pd.set_option('display.max_rows', None)
# pd.options.display.max_columns = None
#------------------------------- READ .CSV FILES--------------------------------
cyclones = pd.read_csv("TROPICAL_DEPRESSIONS_STORMS_AND_HURRICANES_2000_2024.csv")
dfCyclones = pd.DataFrame(cyclones).drop_duplicates()
dfCyclones["CZ_FIPS"] = dfCyclones["CZ_FIPS"].astype(str)

winds = pd.read_csv("TORNADOES_AND_THUNDERSTORM_WINDS_2000_2024.csv")
dfWinds = pd.DataFrame(winds).drop_duplicates()
dfWinds["CZ_FIPS"] = dfWinds["CZ_FIPS"].astype(str)

seaLevels = pd.read_csv("COASTAL_FLOODS_AND_STORM_SURGE_2000_2024.csv")
dfSeaLevels = pd.DataFrame(seaLevels).drop_duplicates()
dfSeaLevels["CZ_FIPS"] = dfSeaLevels["CZ_FIPS"].astype(str)

precip = pd.read_csv("HAIL_AND_FLOOD_2000_2024.csv")
dfPrecip = pd.DataFrame(precip).drop_duplicates()
dfPrecip["CZ_FIPS"] = dfPrecip["CZ_FIPS"].astype(str)

#------------------------------- AGGREGATE EACH DATASET BY COUNTY/ZONE--------------------------------
# Function to construct an aggregate table for count of events, # of deaths, injuries, and property damages
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
#Function Ends--

# CYCLONES (zone):
dfCyclonesByZone = createAggregateTable(dfCyclones,"Zone","Zone_FIPS")
# print(dfCyclonesByZone.columns)

# WINDS (county):
dfWindsByCounty= createAggregateTable(dfWinds,"County","County_FIPS")
# print(dfWindsByCounty)

# SEVERE PRECIPITATION (county & zone): the EVENT_TYPE FLOOD in this file has both county-based and zone based data
dfPrecipByCounty = createAggregateTable(dfPrecip[dfPrecip["CZ_TYPE"] == "C"],"County","County_FIPS") #agg table for data rows by county
dfPrecipByZone = createAggregateTable(dfPrecip[dfPrecip["CZ_TYPE"] == "Z"],"Zone","Zone_FIPS") #agg table for data rows by zone
# print(dfPrecipByCounty)
# print(dfPrecipByZone)

# SEA LEVELS AKA COASTAL INUNDATION (zone):
dfSeaLevelsByZone= createAggregateTable(dfSeaLevels,"Zone","Zone_FIPS")
# print(dfSeaLevelsByZone)

#------------------------------- CONVERT ANY ZONE-BASED DATASET TO COUNTY-BASED --------------------------------
# Read the file containing zone-to-county mapping
cz = pd.read_excel("county_zone_correl.xlsx")
dfCZ = pd.DataFrame(cz)
# print(dfCZ.columns)
dfZoneCounty = dfCZ[dfCZ['STATE']=='AL'][['ZONE','FIPS','COUNTY']] #filter only for AL
dfZoneCounty = dfZoneCounty.rename(columns={'ZONE':'Zone_FIPS','COUNTY':'County'}).reset_index(drop=True) #rename columns for clarity & consistency

# get the county part of the full FIPS codes (5-digit FIPS code, first 2 are state fips, last 3 are county fips):
county_FIPS = []
for _, row in dfZoneCounty.iterrows():
    county_FIPS.append(str(row["FIPS"])[-3:].lstrip('0')) #County_FIPS is the last 3 digits of the FIPS
dfZoneCounty['County_FIPS'] = county_FIPS
dfZoneCounty["Zone_FIPS"] = dfZoneCounty["Zone_FIPS"].astype(str) # make sure it's str dtype
dfZoneCounty = dfZoneCounty.drop('FIPS',axis=1) #drop the full FIPS column

# Function to vlookup the corresponding county of the zone (for datasets categorized by zone instead of county)
def ConvertZoneToCounty (df_by_zone):
    df_by_county = pd.merge(df_by_zone, dfZoneCounty, on="Zone_FIPS", how='left').drop(['Zone_FIPS','Zone'],axis=1)
    #Aggregate data by each unique county (this is needed as 1 county can have multiple zones)
    df_by_county = df_by_county.groupby(["County_FIPS","County"],as_index=False).agg(
        {col: 'sum' for col in df_by_county.select_dtypes(include='number').columns}
    )
    return df_by_county
# Function Ends--

# transform zone-based dfs to county-based dfs (for Sea Levels and Cyclones dfs)
dfSeaLevelsByCounty = ConvertZoneToCounty(dfSeaLevelsByZone)
dfCyclonesByCounty = ConvertZoneToCounty(dfCyclonesByZone)
# Convert the zone-based half of the precipitation df to county-based and concat it into the county-based half
dfPrecipByCounty = pd.concat([dfPrecipByCounty,ConvertZoneToCounty(dfPrecipByZone)],ignore_index=True)
# Aggregate the combined precipdata by each unique county
dfPrecipByCounty = (
    dfPrecipByCounty.groupby(["County","County_FIPS"],as_index=False).agg(
        {col: 'sum' for col in dfPrecipByCounty.select_dtypes(include='number').columns}
    )
)

#--------------------------- COMBINE ALL COUNTY-BASED DFs INTO 1 MASTER DF ----------------------------------
# Create a dfCounty with 67 AL counties based on the zone_county_correl df
dfCounty = dfZoneCounty.drop("Zone_FIPS",axis=1).drop_duplicates()
dfCounty.sort_values(by="County",ascending=True,inplace=True)
dfCounty.reset_index(drop=True, inplace=True)

# Create the master dataset that combines all the severe weather data by county
dfMasterFreq = pd.merge(dfCounty,dfWindsByCounty,on=["County","County_FIPS"],how="left") # merge winds into master df
dfMasterFreq = pd.merge(dfMasterFreq,dfSeaLevelsByCounty,on=["County","County_FIPS"],how="left") # merge sea levels into master df
dfMasterFreq = pd.merge(dfMasterFreq,dfCyclonesByCounty,on=["County","County_FIPS"],how="left") # merge cyclones into master df
dfMasterFreq = pd.merge(dfMasterFreq,dfPrecipByCounty,on=["County","County_FIPS"],how="left") # merge precip into master df

print(dfMasterFreq.columns)
# dfMasterFreq.to_csv("MASTER_FILE_OF_OCCURRENCE_FREQUENCE_AND_CASUALTY_SUMMARY.csv",index=False)

#--------------------------- Calculate the Average magnitude for Tornadoes, Th/Winds, and Hails ----------------------------------

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

def createAggregateTable(df_raw_data, agg_col_name):
    dfAverageMagnitude = (
        df_raw_data.groupby(["County_FIPS", "County"], as_index=False)
        .agg(**{agg_col_name: ("MAGNITUDE", "mean")})
    )
    return dfAverageMagnitude

dfTornadoMagnitude = createAggregateTable(dfTornadoMagnitude,"Avg_Tor_EF")
dfThunderstormWindMagnitude = createAggregateTable(dfThunderstormWindMagnitude,"Avg_ThWind_Speed")
dfHailMagnitude = createAggregateTable(dfHailMagnitude,"Avg_Hail_Size")

dfMasterMag = pd.merge(dfTornadoMagnitude,dfThunderstormWindMagnitude,on=["County","County_FIPS"],how="outer")
dfMasterMag = pd.merge(dfMasterMag,dfHailMagnitude,on=["County","County_FIPS"],how="left")

print(dfMasterMag.columns)
# dfMasterMag.to_csv("MASTER_FILE_OF_CERTAIN_EVENT_INTENSITY.csv",index=False)

#----------------------------------------------------------
