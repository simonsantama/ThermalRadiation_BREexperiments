"""
Interpolates the temperature data over height (1D) and then over a surface to try to understand the three dimensional
temperature distribution

"""

import pickle
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
import pandas as pd

# upload the processed and corrected data
file_address = "Temperatures_Processed_Uncorrected.pkl"
with open(file_address, "rb") as handle:
    all_data = pickle.load(handle)
    
# dictionaries to contain additional data
extra_data = {}

# plotting parameters
colors = ["royalblue", "darkgreen", "firebrick", "blueviolet", "darkorange", "cyan", "black"]*3
linestyles = ["-", "--", "-.", ":"]*4
location_plot = {"TXX": (0,1),
                 "T13": (1,0), "T23": (1,1), "T33": (1,2),
                 "T12": (2,0), "T22": (2,1), "T32": (2,2),
                 "T11": (3,0), "T21": (3,1), "T31": (3,2),
                 "TDD": (4,1)}
    
for test_name in all_data:
    print(test_name)
    
    df = all_data[test_name]
    extra_data[test_name] = {}
    
    # extract all the TC_trees names
    TC_trees_names = []
    for col in df.columns:
        if col == "testing_time":
            pass
        else:
            TC_tree_name = col.split("-")[0]
            TC_trees_names.append(TC_tree_name)
    
    # retain only the unique TC_trees names
    TC_trees = list(set(TC_trees_names))
    
    # iterates over each TC_tree
    for tc_tree in TC_trees:
        thermocouples = []
        thermocouples_heights = []
        extra_data[test_name][tc_tree] = {}
        
        # obtaines a list of all the columns associated to a given tc_tree and also its respective heights
        for col in df.columns:
            if tc_tree in col:
                thermocouples.append(col)
                thermocouples_heights.append(col.split("-")[1])
        
        # convert list of heights from a list of integers to a list of 
        thermocouples_heights = [int(x) for x in thermocouples_heights]
    
        # at every time step, find the maximum and minimum tempeartures and also the height at which that occurrs
        df.loc[:, f"{tc_tree}_max"] = df.loc[:, thermocouples].apply(lambda x: x.values.max(), axis = 1)
        df.loc[:, f"{tc_tree}_height_max"] = df.loc[:, thermocouples].apply(
                lambda x: thermocouples_heights[x.values.argmax()], axis = 1)
        
        df.loc[:, f"{tc_tree}_min"] = df.loc[:, thermocouples].apply(lambda x: x.values.min(), axis = 1)
        df.loc[:, f"{tc_tree}_height_min"] = df.loc[:, thermocouples].apply(
                lambda x: thermocouples_heights[x.values.argmin()], axis = 1)
        
        # also for every tc_tree, I will add the considered heights as well as the maximum and minimum heights
        extra_data[test_name][tc_tree]["all_tcs"] = thermocouples
        
        # for every TC_tree, create a function that interpolates temperature as a function of height
        x = thermocouples_heights
        df.loc[:, f"f_TempvsHeight_{tc_tree}"] = df.loc[:, thermocouples].apply(
                lambda y: interpolate.interp1d(x, y.values), axis = 1)
        
    
    
    
    
#    # First, find a temperature value that is within the interpolating range of ALL trees
#    max_column_list = []
#    min_column_list = []
#    for col in df.columns:
#        if "max" in col:
#            if "height" in col:
#                pass
#            else:
#                max_column_list.append(col)
#        elif "min" in col:
#            if "height" in col:
#                pass
#            else:
#                min_column_list.append(col)
#                
#    # at every time step, determine the temperature range that ALL TC_trees can cover

        
    
#    # now, calculate at every time step the temperature at which we will estimate the height per TC tree
#    min_maximum_temperature = df.loc[:, max_column_list].min(axis = 1)
#    max_minimum_temperature = df.loc[:, min_column_list].max(axis = 1)
#    
##    tracked_temperature = np.round(pd.concat(
##            [min_maximum_temperature, max_minimum_temperature], axis = 1).mean(axis = 1))
#    
#    tracked_temperature = np.ceil(min_maximum_temperature)
#    
#    # calculate the corresponding height at which tracked_temperature is attained for every TC_tree
#    interp_func_list = [x for x in df.columns if "HeightvsTemp" in x]
#    for col in interp_func_list:
#        TC_tree = col.split("_")[2]
#        
#        # very slow implementation but I haven't figured out how to do it with .apply()
#        height_tracked_temperature = np.zeros(len(df))
#        for i,temperature in enumerate(tracked_temperature):
#            print(temperature)
#            height_tracked_temperature[i] = df.loc[i, col](temperature)
#        
#        
##        df.loc[:, f"{TC_tree}_height_tracked_temperature"] = df.loc[:, col].apply(lambda x: print(tracked_temperature))
                
    break

        
        

    # -----------
    # plot maximum and minimum temperature
    # -----------
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
#    # iterate over all the TC_trees in this test
#    for j,tc_tree in enumerate(TC_trees):
#        
#        # extract the name of hte TC tree
#        location = location_plot[tc_tree]
#
#        axis = ax[location[0], [location[1]]][0]
#        y_max = df.loc[:, f"{tc_tree}_max"]
#        y_min = df.loc[:, f"{tc_tree}_min"]
#        x = df.loc[:, "testing_time"]/60
#        
#        axis.plot(x,
#                y_max,
#                color = "steelblue",
#                linewidth = 2,
#                linestyle = "-",
#                label = "max_temperature")
#        
#        axis.plot(x,
#                y_min,
#                color = "crimson",
#                linewidth = 2,
#                linestyle = "-",
#                label = "min_temperature")
#        
#        axis.fill_between(x,
#                          y_max,
#                          y_min,
#                          color = "grey",
#                          alpha = 0.75)
#
#        axis.legend(fancybox = True, loc = "lower right", 
#                    fontsize = 6, ncol = 3)
#        
#        # add a text that indicates which TCs are avaialable
#        ax[0,0].text(x = 5, y = 1300, 
#                      s = "Working TCs per TC tree:",fontsize = 6)
#        
#        
#        text_string = " ".join([x.split('-')[1] for x in tc_columns])
#        text_string = f"{tc_tree}:\n{text_string}"
#        ax[0,0].text(x = 5, y = 1200 - j*150, 
#                  s = text_string,fontsize = 6)
#    
#    # save and close
#    fig.savefig(f"{test_name}_temperatures_maxANDmin_uncorrected.png", dpi = 300)
#    plt.close(fig)
#
#    # -----------
#    # plot height at which the maximum and minimum temperatures are achieved
#    # -----------
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
#        axis.set_ylabel("Height [mm]", fontsize = 8)
#        axis.set_ylim([0,320])
#        axis.set_yticks(np.linspace(20,280,14))
#    for axis in [ax[3,0], ax[4,1], ax[3,2]]:
#        axis.set_xlabel("Time [min]", fontsize = 10)
#        axis.set_xlim([0,60])
#        axis.set_xticks(np.linspace(0,60,5))
#    for axis in [ax[0,0], ax[0,2], ax[4,0], ax[4,2]]:
#        axis.axis("off")
#    
#    # iterate over all the TC_trees in this test
#    for tc_tree in TC_trees:
#        
#        # extract the name of hte TC tree
#        location = location_plot[tc_tree]
#
#        axis = ax[location[0], [location[1]]][0]
#        y_max = df.loc[:, f"{tc_tree}_height_max"]
#        y_min = df.loc[:, f"{tc_tree}_height_min"]
#        x = df.loc[:, "testing_time"]/60
#        
#        axis.plot(x,
#                y_max,
#                color = "steelblue",
#                linewidth = 1,
#                linestyle = "-",
#                label = "height_max_temperature")
#        
#        axis.plot(x,
#                y_min,
#                color = "crimson",
#                linewidth = 1,
#                linestyle = "-",
#                label = "height_min_temperature")
#
#        axis.legend(fancybox = True, loc = "upper right", 
#                    fontsize = 5, ncol = 3)
#    
#    # save and close
#    fig.savefig(f"{test_name}_heights_maxANDmin_uncorrected.png", dpi = 300)
#    plt.close(fig)
    

        
        
    
            
