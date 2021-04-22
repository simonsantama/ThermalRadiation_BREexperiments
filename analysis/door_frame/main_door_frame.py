"""
This script analyses door frame data (pressure probes and temperatures) to
calculate mass flow, neutral plane height and internal HRR.
"""

import pickle

# import my own functions
from data_processing import (calculation_area,
                             calculation_velocity,
                             calculation_massflow,
                             calculation_HRR)

DoorFrame = {}
DoorFrame_full = {}

# dictionaries used to save the data separately in the data processed folder
Velocities = {}
Temperatures = {}
Neutral_Plane = {}
Mass_Flow = {}
HRR_internal_massin = {}    
HRR_internal_juanalyser = {}

# upload the data from the excel spreadsheets
file_address = ("C:/Users/s1475174/Documents/Python_Projects/Thermal"
                r"Radiation_BREexperiments/unprocessed_data/door_frame/D"
                r"oorFrame_unprocessed.pkl")
with open(file_address, "rb") as handle:
    DoorFrame = pickle.load(handle)

# iterate over the four tests to be analysed
for test_name in ["Alpha1","Alpha2", "Beta1", "Beta2", "Gamma"]:
    
    print(f"Analysing experiment {test_name}")
    
    # extract data and divide into temperature/pressure_probe and gas analysis
    df_full = DoorFrame[test_name]
    df = df_full.iloc[:, :22].copy()
    
    # start with analysis of temperature/pressure_probe data
    df.rename(columns = {"Time [min]": "testing_time"}, inplace = True)
    
    # modify testing time to show in seconds
    df.loc[:, "testing_time"] = df.loc[:, "testing_time"] * 60
    
    # calculate areas
    areas = calculation_area()
    
    # calculate velocities
    calculation_velocity(df, test_name)
    
    # calculate massflow
    calculation_massflow(df, areas)
    
    # store in DoorFrame_full for plotting below
    DoorFrame_full[test_name] = df
    
    # save data into independent dictionaries
    v_columns = [col for col in df.columns if "V_" in col]
    m_columns = [col for col in df.columns if "mass_" in col]
    t_columns = [col for col in df.columns if "TC_" in col]
    for lst in [v_columns, m_columns, t_columns]:
        lst.append("testing_time")
    np_columns = ["testing_time", "Neutral_Plane", "Neutral_Plane_Smooth"]
    hrr_massin_columns = ["testing_time", "hrr_internal_allmassin"]
    
    Velocities[test_name] = df.loc[:, v_columns]
    Mass_Flow[test_name] = df.loc[:, m_columns]
    Temperatures[test_name] = df.loc[:, t_columns]
    Neutral_Plane[test_name] = df.loc[:, np_columns]
    HRR_internal_massin[test_name] = df.loc[:, hrr_massin_columns]
    
    # Heat Release Rate calculations
    df_juanalyser = df_full.iloc[:, 23:].copy()
    df_juanalyser.rename(columns = {"Time": "testing_time"},
                         inplace = True)
    df_juanalyser.loc[:, "testing_time"] = df_juanalyser.loc[
        :, "testing_time"]*60
    
    """
    the ignition delay was not added to the spreadsheets for Beta1 and Beta2,
    so I am adding it manually.
    """
    if test_name == "Beta1":
        df_juanalyser.loc[:, "testing_time"] = df_juanalyser.loc[
            :, "testing_time"] - 4*60
    if test_name == "Beta2":
        df_juanalyser.loc[:, "testing_time"] = df_juanalyser.loc[
            :, "testing_time"] - 18*60
    calculation_HRR(df_juanalyser, df)
    
    # save internal HRR data into independent dictionary
    HRR_internal_juanalyser[test_name] = df_juanalyser.loc[
        :, ["testing_time","hrr_internal"]]
    
"""
save velocities, neutral plane, mass flow and internal HRR to the processed
data folder
"""
data_to_save = [Velocities, Neutral_Plane, Mass_Flow, Temperatures,
                HRR_internal_massin, HRR_internal_juanalyser]

for i, data_type in enumerate(data_to_save):
    data_name = ["Velocities", "Neutral_Plane", "Mass_Flow",
                 "Door_Temperatures", "HRR_internal_massin",
                 "HRR_internal_juanalyser"][i]
    file_address_save = (f"C:/Users/s1475174/Documents/Python_Projects/T"
                         f"hermalRadiation_BREexperiments/processed_dat"
                         f"a/{data_name}.pkl")
    with open(file_address_save, 'wb') as handle:
        pickle.dump(data_type, handle)

# save dictionary with all the data
address_doorframe_fulldata = (r"C:/Users/s1475174/Documents/Python_Projects/T"
                              r"hermalRadiation_BREexperiments/processed_dat"
                              r"a/doorframe_ALLdata.pkl")
with open(address_doorframe_fulldata, "wb") as handle:
    pickle.dump(DoorFrame_full, handle)
