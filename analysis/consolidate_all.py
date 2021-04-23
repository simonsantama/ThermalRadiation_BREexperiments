"""
This script loads all the data, interpolates it to a 1Hz data frame and saves
it per experiment into a dictionary, which is then saved as an excel file
"""

import os
import pickle
import numpy as np
import pandas as pd

address_processed_data = (r"C:\Users\s1475174\Documents\Python_Projects\T"
                          r"hermalRadiation_BREexperiments\processed_data")

# create dictionary of dataframes and introduce testing time column
all_data = {"Alpha2": 0, "Beta1": 0, "Beta2": 0, "Gamma": 0}
for experiment in all_data:
    all_data[experiment] = pd.DataFrame()
    all_data[experiment].loc[:, "testing_time"] = np.linspace(0, 3600, 3601)


# interpolate all the data to a 1Hz frequency and copy into data frame
for file in os.listdir(address_processed_data):
    if ".xlsx" in file:
        continue
    with open(os.path.join(address_processed_data, file), "rb") as handle:
        data = pickle.load(handle)
        for experiment in data.keys():
            if experiment == "Alpha1":
                continue
            df = data[experiment]

            # parse door frame data
            if file == "doorframe_ALLdata.pkl":
                for column in df.columns:
                    if ("V_" not in column) and (
                        "mass_in" not in column) and (
                        "mass_out" not in column) and (
                        "Neutral_Plane_Smooth" not in column) and (
                        "hrr_internal_allmassin" not in column):
                        continue
                    else:
                        x = all_data[experiment].loc[:, "testing_time"].values
                        xp = df.loc[:, "testing_time"].values
                        fp = df.loc[:, column].astype("float64").values
                        all_data[experiment].loc[:, column] = np.interp(
                            x, xp, fp)

            # parse flame dimensions data
            if file == "Flame_Dimensions.pkl":
                for column in df.columns:
                    if ("time" in column) or ("ellipse" in column):
                        continue
                    elif ("smooth" not in column):
                        continue
                    else:
                        x = all_data[experiment].loc[:, "testing_time"].values
                        xp = df.loc[:, "testing_time"].values
                        fp = df.loc[:, column].astype("float64").values
                        all_data[experiment].loc[:, column] = np.interp(
                            x, xp, fp)

# save data into an excel file
with pd.ExcelWriter (os.path.join(address_processed_data,
                                  "all_data_BREexperiments.xlsx")) as writer:
    for experiment in all_data:
        df = all_data[experiment]
        df.to_excel(writer, sheet_name=experiment)