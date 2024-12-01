# magnum_opus
This is a repository for analyzing the hazardous weather across the State of Alabama.
The data is collected from the NOAA Storm Event Database: https://www.ncdc.noaa.gov/stormevents/
The data is organized into 4 major datasets for ease of organization:
    (1) TROPICAL_DEPRESSION_STORMS_AND_HURRICANES_2000_2024: Data of Tropical Cyclones (Hurricane, Tropical Storm, Tropical Depression) from 2000 to 2024
    (2) TORNADOES_AND_THUNDERSTORM_WINDS_2000_2024: Data of Hazardous Winds (Tornado, Thunderstorm Wind) from 2000 to 2024
    (3) COASTAL_FLOODS_AND_STORM_SURGE_2000_2024: Data of Coastal Inundation Events (Coastal Floods, Storm Surge/Tide) from 2000 to 2024
    (4) HAIL_AND_FLOOD_2000_2024: Data of Severe Precipitation Events (Hail, Flood) from 2000 to 2024

There are several inconsistencies across the datasets that the DataCleanser.py file aims to address:
    --> Datasets (1) & (3) list the storm events by the NWS Public Forecast Zones (https://www.weather.gov/gis/publiczones)
    --> Datasets (2) lists the storm events by the state county
    --> Datasets (4) lists the flood events by both zone and county but the hail events only by county
    --> 1 county can have multiple zones (in AL, just Mobile and Baldwin counties have zones)

# create virtual environment to use python in VSCode
py -m venv myvenv
.\myvenv\Scripts\activate
pip install <package>

# to read excel files w/ Pandas:
pip install openpyxl