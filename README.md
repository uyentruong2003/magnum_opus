# magnum_opus
This is a repository for analyzing the hazardous weather across the State of Alabama

# create virtual environment to use python in VSCode
py -m venv myvenv
.\myvenv\Scripts\activate
pip install <package>

# to read excel files w/ Pandas:
pip install openpyxl

# Draft codes archived:
    # dfAggregate[FIPS_type] = df_raw_data['CZ_FIPS']
    # dfAggregate[loc_type] = df_raw_data['CZ_NAME_STR']
    # dfAggregate.drop_duplicates(inplace=True)
    # metrics = {
    #     "Count": lambda df, row, event: len(df[(df["CZ_FIPS"] == row[FIPS_type]) & (df["EVENT_TYPE"] == event)]),
    #     "Deaths": lambda df, row, event: df[(df["CZ_FIPS"] == row[FIPS_type]) & (df["EVENT_TYPE"] == event)]['DEATHS_DIRECT'].sum(),
    #     "Injuries": lambda df, row, event: df[(df["CZ_FIPS"] == row[FIPS_type]) & (df["EVENT_TYPE"] == event)]['INJURIES_DIRECT'].sum(),
    #     "PropertyDamages": lambda df, row, event: df[(df["CZ_FIPS"] == row[FIPS_type]) & (df["EVENT_TYPE"] == event)]['DAMAGE_PROPERTY_NUM'].sum(),
    # }

    # # Initialize empty dictionaries to store results for each metric
    # results = {metric: {event: [] for event in event_type_list} for metric in metrics.keys()}

    # # Iterate over each row in dfAggregate
    # for _, row in dfAggregate.iterrows():
    #     for event in event_type_list:
    #         for metric, func in metrics.items():
    #             results[metric][event].append(func(df_raw_data, row, event))

    # # Add results to dfAggregate
    # for metric, event_data in results.items():
    #     for event, values in event_data.items():
    #         column_name = f"{event.replace(' ', '')}_{metric}"
    #         dfAggregate[column_name] = values

    # return dfAggregate