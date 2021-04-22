"""
Plots the raw and processed data from the door frame to evaluate the algorithm
and identify broken sensors
"""

import pickle
import matplotlib.pyplot as plt
import numpy as np


# Plotting of the raw data to evaluate the algorithm and identify any broken sensors
test_name = ["Alpha1",
              "Alpha2", 
              "Beta1", 
              "Beta2", 
              "Gamma"]
y_labels = ["Temperature [$^\circ$C]",
            "Transducers [V]",
            "Transducers [V]",
            "DeltaP [Pa]",
            "DeltaP [Pa]",
            "Temperature [$^\circ$C]",
            "Density [kg/m$^3$]",
            "Velocity [m/s]",
            "Neutral Plane [m]",
            "Neutral Plane Smooth [m]",
            "Mass Flow [kg/s]",]
y_limits = ([0,1200],
            [0,15],
            [-5,5],
            [-20,20],
            [-20,20],
            [0,1200],
            [0, 1.5],
            [-15,5],
            [0,2],
            [0,2],
            [0,1.5])
column_numbers = ([1,9],
                  [10,23],
                  [23,36],
                  [49,62],
                  [62,71],
                  [71,80],
                  [80,89],
                  [89,98],
                  [98, 99],
                  [99,100],
                  [109,112])

address_doorframe_fulldata = (r"C:/Users/s1475174/Documents/Python_Projects/T"
                              r"hermalRadiation_BREexperiments/processed_dat"
                              r"a/doorframe_ALLdata.pkl")
with open(address_doorframe_fulldata, "rb") as handle:
    doorframe_fulldata = pickle.load(handle)

# iterate over all the parameters I wish to plot
fontsize_legend = 6
if False:
    for j, parameter in enumerate(["Raw_Temperatures",
                                    "Raw_PressureProbes",
                                    "Zeroed_PressureProbes",
                                    "DeltaPressure_Smooth",
                                    "DeltaPressure_Smooth_Clean",
                                    "Temperatures_Processed",
                                    "Density",
                                    "Velocity",
                                    "Neutral Plane",
                                    "Neutral_Plane_Smooth",
                                    "Mass Flow"]):    
    
        fig, ax = plt.subplots(5,1,figsize = (8,11), sharex = True)
        fig.suptitle(parameter)
        fig.subplots_adjust(top = 0.9)
        
        ax[4].set_xlim([0,60])
        ax[4].set_xticks(np.linspace(0,60,13))
        ax[4].set_xlabel("Time [min]")
        
        for i, axis in enumerate(ax):
            # format the subplots
            axis.set_ylabel(y_labels[j])
            axis.set_ylim(y_limits[j])
            axis.grid(True, linestyle = "--", color = "gainsboro")
            axis.set_title(test_name[i])
    
            # extract data
            df = doorframe_fulldata[test_name[i]]
    
            # plot
            mask = (df.loc[:, "testing_time"] > 0) & (df.loc[
                :,"testing_time"]/60 < 60)
            for column in df.columns[
                    column_numbers[j][0]:column_numbers[j][1]]:
                axis.plot(df.loc[:, "testing_time"]/60,
                          df.loc[:, column],
                          label = column)
            axis.legend(fancybox = True, ncol = 4, fontsize = fontsize_legend)
        
        fig.savefig(r"C:\Users\s1475174\Documents\Python_Projects\Thermal"
                    r"Radiation_BREexperiments\plotting\onevariable_all"
                    f"experiments/{parameter}.png", dpi = 600)
        plt.close(fig)
    
# Plot to show the velocities as a function of time at different heights
if True:
    fig, ax = plt.subplots(1,5,figsize = (14,8), sharex = True, sharey = True)
    ax[0].set_ylim([0,2])
    ax[0].set_yticks(np.linspace(0,2,6))
    ax[0].set_ylabel("Height [m]")
    
    for i,axis in enumerate(ax):
        # format the subplots
        axis.grid(True, linestyle = "--", color = "gainsboro")
        axis.set_title(test_name[i])
        axis.set_xlim([-15,5])
        axis.set_xticks(np.linspace(-15,5,5))
        axis.set_xlabel("Velocity [m/s]")
        
        # extract data
        df = doorframe_fulldata[test_name[i]]
        
        heights = [0.2,0.4,0.6,0.8,1.0,1.2,1.4,1.6,1.8]
        times_of_interest = [5,10,15, 20, 25, 30]
        
        for j,t in enumerate(times_of_interest):
            mask = df.loc[:,"testing_time"]/60 > t
            index = df.loc[mask, :].index[0]
            velocity = df.loc[index, df.columns[89:98]].values
            
            # plot
            axis.plot(velocity,
                    heights,
                    label = f"{t} min",
                    linestyle = (["-", "--", "-.", ":"] * 3)[j])
        axis.legend(fancybox = True, ncol = 1, fontsize = fontsize_legend,
                    title = "Time")
    
    fig.savefig(r"C:\Users\s1475174\Documents\Python_Projects\Thermal"
                r"Radiation_BREexperiments\plotting\onevariable_all"
                r"experiments\velocity_vs_height.png",
                dpi = 600)
    plt.close(fig)


    
    