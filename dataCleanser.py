import pandas as pd
import numpy as np

cyclones = pd.read_csv("TROPICAL_DEPRESSIONS_STORMS_AND_HURRICANES_2000_2024_ALL.csv")
dfCyclones = pd.DataFrame(cyclones)
dfCyclones.drop_duplicates()
print(dfCyclones.columns)

winds = pd.read_csv("TORNADOES_AND_THUNDERSTORM_WINDS_2000_2024_ALL.csv")
dfWinds = pd.DataFrame(winds)
dfWinds.drop_duplicates()

seaLevels = pd.read_csv("COASTAL_FLOODS_AND_STORM_SURGE.csv")
dfSeaLevels = pd.DataFrame(seaLevels)
dfSeaLevels.drop_duplicates()


#This is a function to construct a summary table for count of events, # of deaths, injuries, and property damages
def createSummaryTable(df_raw_data, event_type_list):
    dfSummary = pd.DataFrame()
    dfSummary["FIPS"] = df_raw_data['CZ_FIPS']
    dfSummary['Counties'] = df_raw_data['CZ_NAME_STR']
    dfSummary.drop_duplicates(inplace=True)
    metrics = {
        "Count": lambda df, row, event: len(df[(df["CZ_FIPS"] == row["FIPS"]) & (df["EVENT_TYPE"] == event)]),
        "Deaths": lambda df, row, event: df[(df["CZ_FIPS"] == row["FIPS"]) & (df["EVENT_TYPE"] == event)]['DEATHS_DIRECT'].sum(),
        "Injuries": lambda df, row, event: df[(df["CZ_FIPS"] == row["FIPS"]) & (df["EVENT_TYPE"] == event)]['INJURIES_DIRECT'].sum(),
        "PropertyDamages": lambda df, row, event: df[(df["CZ_FIPS"] == row["FIPS"]) & (df["EVENT_TYPE"] == event)]['DAMAGE_PROPERTY_NUM'].sum(),
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


# CYCLONES (county):
cyclone_event_types = ["Hurricane", "Tropical Storm", "Tropical Depression"]
dfCyclonesSummary = createSummaryTable(dfCyclones,cyclone_event_types)
print(dfCyclonesSummary)


# WINDS (zone):
wind_event_types = ["Tornado", "Thunderstorm Wind"]
dfWindsSummary= createSummaryTable(dfWinds, wind_event_types)
print(dfWindsSummary)
#Including Magnitudes (EF scale for tornadoes, and knotts or Beaufort scale for thunderstorm winds)

# HAIL (zone):
#Including Magnitudes (inches)

# FLOOD (county):

# SEA LEVELS (county):
seaLevel_event_types = ["Coastal Flood","Storm Surge/Tide"]
dfSeaLevelsSummary= createSummaryTable(dfSeaLevels, seaLevel_event_types)
print(dfSeaLevelsSummary)
