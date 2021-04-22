"""
Plots for proposal. Rory. July 2020.
This script takes the data from Alpha2, Beta 1 and Gamma.
Plots the data at a height of two meters for different tests
"""
#import libraries
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
from matplotlib import cm
import numpy as np
import pickle
from scipy import interpolate

# import data
file_address = "condensed_data.pickle"
with open(file_address, "rb") as handle:
    all_condensed_data = pickle.load(handle)

colors1 = cm.get_cmap("cividis", 7)
line_styles = ["-", "--", "-.", ":"]*2

# iterate over different experiments
for experiment_number, experiment in enumerate(all_condensed_data):
    temperatures = all_condensed_data[experiment]
    
    list_columns_at_desiredheight = []    
    for column in temperatures:
        if column != "testing_time":
            height = int(column.split("-")[1])
            if height == 180:
                list_columns_at_desiredheight.append(column)
                
    
    # figure 1: just plot all the temperatures vs time
    fig, ax = plt.subplots(1,1,figsize = (5,3.5), constrained_layout = True)
    ax.set_xlabel("Time [$s$]", fontsize = 11)
    ax.set_xlim([0,60])
    ax.set_xticks(np.linspace(0,60,5))
    ax.set_ylabel("Temperature [$^\circ$C]", fontsize = 11)
    ax.set_ylim([0,1500])
    ax.set_yticks(np.linspace(0,1500,6))
    ax.grid(True, color = "gainsboro", linewidth = 0.5, linestyle = "--")
    ax.set_title(f"Configuration {['Alpha', 'Beta', 'Gamma'][experiment_number]}.\nTest {[2,1,1][experiment_number]}. Height 1.8 m.", 
                                  fontsize = 12)
    

    # inset to show location of the thermocouples
    inset = inset_axes(ax, width="30%", height="30%", loc=["lower right", "upper right", "lower right"][experiment_number], 
                       borderpad = 1)
    inset.set_ylim([0,3])
    inset.set_xlim([0,3])
    inset.set_xticks([0,1,2,3])
    inset.set_yticks([0,1,2,3])
    inset.grid(True, linestyle = "--", linewidth = 0.4, color = "gainsboro")
    inset.xaxis.set_ticklabels([])
    inset.yaxis.set_ticklabels([])
    inset.xaxis.set_ticks_position('none')
    inset.yaxis.set_ticks_position('none')
#    inset.xaxis.set_visible(False)
#    inset.yaxis.set_visible(False)
    
    all_lines = []
    all_locations = []
    for column in list_columns_at_desiredheight:
        location = column.split("-")[0]
        # rename the locations to something that it is easier to read
        if location == "T11":
            text = "LN"
            linecolor = colors1(0)
            style = line_styles[0]
            pos = (0.5,0.5)
        elif location == "T13":
            text = "LF"
            linecolor = colors1(1/7)
            style = line_styles[1]
            pos = (0.5, 2.5)
        elif location == "TD":
            text = "D"
            pos = (1.5,0.4)
            linecolor = colors1(2/7)
            style = line_styles[2]
        elif location == "T22":
            text = "C"
            linecolor = colors1(3/7)
            style = line_styles[3]
            pos = (1.5,1.5)
        elif location == "TXX":
            text = "W"
            linecolor = colors1(4/7)
            style = line_styles[4]
            pos = (1.5, 2.65)
        elif location == "T31":
            text = "RN"
            linecolor = colors1(5/7)
            style = line_styles[5]
            pos = (2.5, 0.5)
        elif location == "T33":
            text = "RF"
            linecolor = colors1(6/7)
            style = line_styles[6]
            pos = (2.5,2.5)
        
        all_locations.append(location)
        
        # plot temperature lines
        ax.plot(temperatures.loc[:, "testing_time"]/60,
                    temperatures.loc[:, column],
                    linewidth = 1.25,
                    color = linecolor,
                    linestyle = style)
        
        # plot thermocouple locations
        inset.scatter(pos[0],
                      pos[1],
                      marker = "o",
                      color = linecolor,
                      s = 12)
        
        
        inset_text_x = [0.4,0.4,1.4,1.65,1.4,2.4,2.4,2.4]
        inset_text_y = [0.75,2,0.65,1.5,2.2,0.75,2]
        if experiment == "Alpha2":
            # plot rectangles that indicate the location of the exposed timber
            inset.fill_between([0,3],[2.8,2.8],[3,3], color = "wheat")
            inset.fill_between([0,0.15],[0,0],[3,3], color = "wheat")
            inset.fill_between([1.25,1.75], [0,0], [0.1,0.1], color = "maroon")
            
            legend_text = ["Left Near", "Left Far", "Door", "Centre", "Right Near", "Right Far"]
            inset_text = ["LN", "LF", "D", "C", "RN", "RF"]
            inset_text_x = [0.4,0.4,1.4,1.65,2.4,2.4]
            inset_text_y = [0.75,2,0.65,1.5,0.75,2]
        elif experiment == "Beta1":
            inset.fill_between([0,3],[2.8,2.8],[3,3], color = "wheat")
            inset.fill_between([1.25,1.75], [0,0], [0.1,0.1], color = "maroon")
            
            legend_text = ["Left Near", "Left Far", "Door", "Centre", "Wall", "Right Near", "Right Far"]
            inset_text = ["LN", "LF", "D", "C", "W", "RN", "RF"]

        elif experiment == "Gamma":
            inset.fill_between([0,3],[2.8,2.8],[3,3], color = "wheat")
            inset.fill_between([0,0.15],[0,0],[3,3], color = "wheat")
            inset.fill_between([1.25,1.75], [0,0], [0.1,0.1], color = "maroon")
            
            legend_text = ["Left Near", "Left Far", "Door", "Centre", "Wall", "Right Near", "Right Far"]
            inset_text = ["LN", "LF", "D", "C", "W", "RN", "RF"]

    all_lines = []
    for i, text in enumerate(legend_text):
        l, = ax.plot([],[], color = colors1(i,7), linewidth = 1.25, linestyle = line_styles[i])
        all_lines.append(l)
        
    for i, text in enumerate(inset_text):
        inset.text(inset_text_x[i],
                   inset_text_y[i],
                   text,
                   fontsize = 7)
        
    
    ax.legend(all_lines, legend_text, fancybox = True, loc = [(0.1,0.05), "center right",
                                                              (0.1,0.05)][experiment_number], fontsize = 7,
              ncol = 2)
    
    plt.savefig(f"{experiment}.png", dpi = 900)
    plt.close()
    
    
    # contour plot to show the variation in space at a given time
    if experiment == "Beta1":
        continue
    else:
        # create plot
        fig, ax = plt.subplots(1,1,figsize = (5,3.5))
        ax.tick_params(axis='both', which='major', labelsize=8)
        ax.set_xlabel("Width [$m$]", fontsize = 11)
        ax.set_ylabel("Length [$m$]", fontsize = 11)
        ax.set_title(f"Configuration {['Alpha', '','Gamma'][experiment_number]}. Test {[2,0,1][experiment_number]}" +\
                                      "\nHeight 1.8 m. Time: 10 min", fontsize = 12)
        ax.set_xlim([0,2.72])
        ax.set_ylim([0,2.72])
        
        # plot the locations of the thermocouples
        positions = [(0.25,0.25),(0.25,2.47),(1.36,0.1),(1.36,1.36),(1.36,2.62),(2.47,0.25),(2.47,2.47)]
        for i,pos in enumerate(positions):
            if (experiment == "Alpha2") and (i == 4):
                continue
            elif (experiment == "Gamma") and (i == 5):
                continue
            ax.scatter(pos[0],
                          pos[1],
                          marker = "o",
                          color = "maroon",
                          alpha = 0.65,
                          s = 10, 
                          zorder = 2)
        
        # define x and y for 2D interpolation
        x,y = list(zip(*positions))
        temperatures_givenheight = np.zeros(6)
        if experiment == "Alpha2":
            x = x[0:4] + x[5:]
            y = y[0:4] + y[5:]
        if experiment == "Gamma":
            x = x[0:5] + x[6:]
            y = y[0:5] + y[6:]

        # quick and dirty implementation to extract the temperature (z) data for 2D interpolation
        for column in list_columns_at_desiredheight:
            location = column.split("-")[0]
            if location == "T11":
                temperatures_givenheight[0] = temperatures.loc[600, column]
            elif location == "T13":
                temperatures_givenheight[1] = temperatures.loc[600, column]
            elif location == "TD":
                temperatures_givenheight[2] = temperatures.loc[600, column]
            elif location == "T22":
                temperatures_givenheight[3] = temperatures.loc[600, column]
                
            # alpha2 has no wall temperatures
            if experiment == "Alpha2":
                if location == "T31":
                    temperatures_givenheight[4] = temperatures.loc[600, column]
                elif location == "T33":
                    temperatures_givenheight[5] = temperatures.loc[600, column]
                    
            elif experiment == "Gamma":
                if location == "TXX":
                    temperatures_givenheight[4] = temperatures.loc[600, column]
                elif location == "T33":
                    temperatures_givenheight[5] = temperatures.loc[600, column]            

        # interpolate
        f = interpolate.interp2d(x,y,temperatures_givenheight)
        
        # define new x and y and apply the interpolated function to it
        x_new = np.linspace(0,2.72,100)
        y_new = np.linspace(0,2.72,100)
        xx, yy = np.meshgrid(x,y)
        new_temperatures = f(x_new, y_new)
        
        # contour plots
        norm = mpl.colors.Normalize(vmin = 800, vmax = 1100)
        cf = ax.contourf(x_new, y_new, new_temperatures, levels = 10, cmap = "cividis", vmin = 800, vmax = 1100)
        fig.subplots_adjust(right=0.85)
        
        
        cb_ax = fig.add_axes([0.86, 0.12, 0.04, 0.76])
        cbar = mpl.colorbar.ColorbarBase(cb_ax, cmap = mpl.cm.cividis, norm = norm, ticks = [800,900,1000,1100])
        cbar.set_label("Temperature [$^\circ$C]", fontsize = 8)
        cbar.ax.tick_params(labelsize=7)
        
        # plot location of timber and door
        ax.fill_between([0,2.72],[2.65,2.65], [2.72,2.72], facecolor = "wheat", alpha = 0.9)
        ax.fill_between([0,0.04],[0,0], [2.65,2.65], facecolor = "wheat", alpha = 0.9)
        ax.fill_between([1.2,1.52],[0,0], [0.05,0.05], color = "black", alpha = 0.8)
        
        plt.savefig(f"Contour_{experiment}.10min.png", dpi = 900)
        
        
    
        
    
