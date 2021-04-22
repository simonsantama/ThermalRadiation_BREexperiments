"""
This script integrates all thermocouple readings into one dataframe per experiments and then
corrects those readings for radiation.

"""


# import libraries
import numpy as np
import pickle
import pandas as pd
from scipy import interpolate

# import data
file_address = "Temperatures_Raw.pkl"
with open(file_address, "rb") as handle:
    all_raw_data = pickle.load(handle)

# import door data
file_address = "C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/Door_Temperatures.pkl"
with open(file_address, "rb") as handle:
    door_temperatures = pickle.load(handle)

list_useful_cols = [f"T{x}" for x in [11,12,13,21,22,23,31,32,33,"XX", "DD"]]
all_useful_cols = {name:[] for name in list_useful_cols}

# reduce all the data


#processed_data = {}
#
## plot
#for test_name in ["Alpha2", "Beta1", "Beta2", "Gamma"]:
#    
#    print(test_name)
#    data_dict = all_raw_data[test_name]
#    data_door = door_temperatures[test_name]
#    
#    condensed_data = pd.DataFrame()
#    condensed_data["testing_time"] = np.linspace(0,3600,3601)
#    
#    for logger in data_dict:
#        df = data_dict[logger]
#        
#        # eliminate the broken TCs
#        if test_name == "Alpha2":
#            erase_cols = ["T12-240","T12-260", "T31-100"]
#        if test_name == "Beta1":
#            erase_cols = ["T11-80", "T11-100","T11-140", "T12-140", "T32-140", "T32-160",
#                          "T32-180","T32-200", "T32-220", "T32-260"]
#        if test_name == "Beta2":
#            erase_cols = ["T22-180", "T11-240", "T11-260", "T12-240", "T12-260", "T23-260",
#                          "T23-220"]
#        if test_name == "Gamma":
#            erase_cols = ["T11-80", "T11-100", "T11-140", "T12-140", "T12-240", "T12-260",
#                          "T23-80","T23-100", "T23-120","T23-140", "T23-160", "T23-180", "T23-200","T23-220","T23-240","T23-260", 
#                          "T21-40"]
#        
#        # getting rid of the columns with non-formatted names
#        drop_columns = [col for col in df.columns if "<" in col]
#        df.drop(columns = drop_columns, inplace = True)
#        
#        # getting rid of broken TCs
#        for column in df.columns:
#            if column in erase_cols:
#                df.drop(columns = column, inplace = True)
#        
#        # mask for testing time (0 to 60 minutes)
#        mask = (df.loc[:, "testing_time"]/60 > 0) & (df.loc[:, "testing_time"]/60 < 60)
#
#        for column in df.columns[1:]:
#            x = df.loc[mask, "testing_time"]
#            y = df.loc[mask, column]
#            f = interpolate.interp1d(x,y, kind = "linear", fill_value = "extrapolate")
#            condensed_data[column] = f(condensed_data.loc[:, "testing_time"])
#     
#    # do the same interpolation for the door data
#    mask = (data_door.loc[:, "testing_time"]/60 > 0) & (data_door.loc[:, "testing_time"]/60 < 60)
#    for column in data_door:
#        if "testing_time" in column:
#            pass
#        else:
#            x = data_door.loc[mask, "testing_time"]
#            y = data_door.loc[mask, column]
#            g = interpolate.interp1d(x,y, kind = "linear", fill_value = "extrapolate")
#            condensed_data[f"TDD-{column.split('_')[1]}"] = g(condensed_data.loc[:, "testing_time"])
#            
#    # 1 data frame per test with all the data
#    processed_data[test_name] = condensed_data
#        
#    # plot
#    fig, ax = plt.subplots(5,3,figsize = (11,11), sharex = True, sharey = True)
#    fig.subplots_adjust(top = 0.9, left = 0.1, bottom = 0.1,
#                        hspace = 0.2, wspace = 0.075)
#    fig.suptitle(test_name, fontsize = 14)
#    
#    # format plots
#    for j,axis in enumerate(ax.flatten()):
#        axis.grid(True, color = "gainsboro", linestyle = "--", linewidth = 0.75)
#        axis.set_title(["","TXX_CentreWall","",
#                        "T13_LeftFar","T23_CentreFar","T33_RightFar",
#                        "T12_LeftMid","T22_CentreMid","T32_RightMid",
#                        "T11_LeftNear","T21_CentreNear","T31_RightNear",
#                        "", "TDD_Door", ""][j],
#                       fontsize = 12)
#    # format the axis
#    for axis in [ax[0,1], ax[1,0], ax[2,0], ax[3,0], ax[4,1]]:
#        axis.set_ylabel("Temperature [$^\circ$C]", fontsize = 10)
#        axis.set_ylim([0,1400])
#        axis.set_yticks(np.linspace(0,1400,5))
#    for axis in [ax[3,0], ax[4,1], ax[3,2]]:
#        axis.set_xlabel("Time [min]", fontsize = 10)
#        axis.set_xlim([0,60])
#        axis.set_xticks(np.linspace(0,60,5))
#    for axis in [ax[0,0], ax[0,2], ax[4,0], ax[4,2]]:
#        axis.axis("off")
#    
#    # plot
#    for useful_col in list_useful_cols:
#        
#        # extract the name of hte TC tree
#        location = location_plot[useful_col]
#
#        # create a list of columns that correspond to this TC tree
#        TC_tree_columns = [x for x in condensed_data.columns[:] if useful_col in x]
#    
#        axis = ax[location[0], [location[1]]][0]
#        for j, column_name in enumerate(TC_tree_columns):
#            
#            if "testing_time" in column_name:
#                pass
#            else:
#                axis.plot(condensed_data.loc[:, "testing_time"]/60,
#                          condensed_data.loc[:, column_name],
#                          color = colors[j],
#                          linestyle = linestyles[j],
#                          label = column_name.split("-")[1])
#        axis.legend(fancybox = True, loc = "lower right", fontsize = 6, title = "TC Height", ncol = 3)
#    
#    # save and close
#    fig.savefig(f"clean_data_uncorrected/{test_name}_temperatures_processed_uncorrected.png", dpi = 300)
#    plt.close(fig)
#
## save condensed, un_corrected data to a pickle
#file_address = "Temperatures_Clean_Uncorrected.pkl"
#with open(file_address, "wb") as handle:
#    pickle.dump(processed_data, handle)
#
