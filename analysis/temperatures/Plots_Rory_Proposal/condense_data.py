"""
Plots for proposal. Rory. July 2020.
This script takes the data from Alpha2, Beta 1 and Gamma.
Condenses the data into one data frame.
Saves the data as a condensed_data.pickle
"""

# import libraries
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pickle
import time
import pandas as pd

# import data
file_address = "Temperatures_Raw.pkl"
with open(file_address, "rb") as handle:
    all_raw_data = pickle.load(handle)
    
# import doorway data (this is processed in the Door Frame script. It is assumed that air coming - from pressure probe
# data - is at ambient temperature)
file_address = "C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/Door_Temperatures.pkl"
with open(file_address, "rb") as handle:
    door_data = pickle.load(handle)

list_of_experiments = ["Alpha2", "Beta1", "Gamma"]
height = 2 

all_condensed_data = {}
for experiment in list_of_experiments:
    start = time.time()
    
    print(f"Condensing data of {experiment} into a single data frame")
    all_condensed_data[experiment] = pd.DataFrame()
    new_time = np.linspace(0,3600,3601)
    all_condensed_data[experiment].loc[:,"testing_time"] = new_time
    
    # interpolate door data to 1 Hz frequency
    door_temperatures = door_data[experiment]
    for column in door_temperatures:
        if column != "testing_time":
            old_time = door_temperatures["testing_time"]
            old_temperature = door_temperatures[column]
            new_temperature = np.interp(new_time, old_time, old_temperature)
            
            # save the interpolated data in the condensed data frame
            new_column_name = "TD-" + column.split("_")[1]
            all_condensed_data[experiment][new_column_name] = new_temperature
    
    # interpolate the compartment data to 1Hz frequency
    compartment_temperatures = all_raw_data[experiment]
    for logger in compartment_temperatures:
        for column in compartment_temperatures[logger]:
            if column != "testing_time":
                if "<" not in column:
                    old_time = compartment_temperatures[logger]["testing_time"]
                    old_temperature = compartment_temperatures[logger][column]
                    new_temperature = np.interp(new_time, old_time, old_temperature)
                    
                    # save the interpolated data in the condensed data frame
                    all_condensed_data[experiment][column] = new_temperature

with open("condensed_data.pickle", "wb") as handle:
    pickle.dump(all_condensed_data, handle)