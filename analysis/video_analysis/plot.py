"""
Plots results from the image analysis
"""

import pickle
import matplotlib.pyplot as plt
import numpy as np


# load data
file_address_load = (r"C:/Users/s1475174/Documents/Python_Projects/ThermalRad"
                     r"iation_BREexperiments/processed_data/Flame_Dimens"
                     r"ions.pkl")
with open(file_address_load, 'rb') as handle:
    all_data = pickle.load(handle)



test_name = ["Alpha2", "Beta1", "Beta2", "Gamma"]
fontsize_legend = 6   

# plot flame heights
fig, ax = plt.subplots(4,1,figsize = (8,11), sharex = True)
fig.suptitle("Flame heights")
fig.subplots_adjust(top = 0.9)
ax[3].set_xlim([0,60])
ax[3].set_xticks(np.linspace(0,60,13))
ax[3].set_xlabel("Time [min]")

for i, axis in enumerate(ax):
    # format the subplots
    axis.set_ylabel("Flame height [m]")
    axis.set_ylim([0, 5])
    axis.grid(True, linestyle = "--", color = "gainsboro")
    axis.set_title(test_name[i])
    # extract data
    df = all_data[test_name[i]]
    # plot
    mask = (df.loc[:, "testing_time"] > 0) & (df.loc[
        :,"testing_time"]/60 < 60)
    for column in df.columns:
        if "smooth" not in column:
            continue
        if "height" in column:
            axis.plot(df.loc[:, "testing_time"]/60,
                      df.loc[:, column],
                      label=column)
    axis.legend()
fig.savefig(r"C:\Users\s1475174\Documents\Python_Projects\Thermal"
            r"Radiation_BREexperiments\plotting\onevariable_all"
            r"experiments/Flame_heights.png", dpi = 600)
plt.close(fig)

# plot flame depth
fig, ax = plt.subplots(4,1,figsize = (8,11), sharex = True)
fig.suptitle("Flame depth")
fig.subplots_adjust(top = 0.9)
ax[3].set_xlim([0,60])
ax[3].set_xticks(np.linspace(0,60,13))
ax[3].set_xlabel("Time [min]")

for i, axis in enumerate(ax):
    # format the subplots
    axis.set_ylabel("Flame depth [m]")
    axis.set_ylim([0, 2])
    axis.grid(True, linestyle = "--", color = "gainsboro")
    axis.set_title(test_name[i])
    # extract data
    df = all_data[test_name[i]]
    # plot
    mask = (df.loc[:, "testing_time"] > 0) & (df.loc[
        :,"testing_time"]/60 < 60)
    for column in df.columns:
        if "smooth" not in column:
            continue
        if "depth" in column:
            axis.plot(df.loc[:, "testing_time"]/60,
                      df.loc[:, column],
                      label=column)
    axis.legend()
fig.savefig(r"C:\Users\s1475174\Documents\Python_Projects\Thermal"
            r"Radiation_BREexperiments\plotting\onevariable_all"
            r"experiments/Flame_depths.png", dpi = 600)
plt.close(fig)
    
# plot flame area
fig, ax = plt.subplots(4,1,figsize = (8,11), sharex = True)
fig.suptitle("Flame area")
fig.subplots_adjust(top = 0.9)
ax[3].set_xlim([0,60])
ax[3].set_xticks(np.linspace(0,60,13))
ax[3].set_xlabel("Time [min]")

for i, axis in enumerate(ax):
    # format the subplots
    axis.set_ylabel("Flame area [m2]")
    axis.set_ylim([0, 3])
    axis.grid(True, linestyle = "--", color = "gainsboro")
    axis.set_title(test_name[i])
    # extract data
    df = all_data[test_name[i]]
    # plot
    mask = (df.loc[:, "testing_time"] > 0) & (df.loc[
        :,"testing_time"]/60 < 60)
    for column in df.columns:
        if "smooth" not in column:
            continue
        if "area" in column:
            axis.plot(df.loc[:, "testing_time"]/60,
                      df.loc[:, column],
                      label=column)
    axis.legend()
fig.savefig(r"C:\Users\s1475174\Documents\Python_Projects\Thermal"
            r"Radiation_BREexperiments\plotting\onevariable_all"
            r"experiments/Flame_area.png", dpi = 600)
plt.close(fig)

# plot flame projection
fig, ax = plt.subplots(4,1,figsize = (8,11), sharex = True)
fig.suptitle("Projection of top of flame")
fig.subplots_adjust(top = 0.9)
ax[3].set_xlim([0,60])
ax[3].set_xticks(np.linspace(0,60,13))
ax[3].set_xlabel("Time [min]")

for i, axis in enumerate(ax):
    # format the subplots
    axis.set_ylabel("Flame projection [m]")
    # axis.set_ylim([0, 2])
    axis.grid(True, linestyle = "--", color = "gainsboro")
    axis.set_title(test_name[i])
    # extract data
    df = all_data[test_name[i]]
    # plot
    mask = (df.loc[:, "testing_time"] > 0) & (df.loc[
        :,"testing_time"]/60 < 60)
    for column in df.columns:
        if "smooth" not in column:
            continue
        if "projection" in column:
            axis.plot(df.loc[:, "testing_time"]/60,
                      df.loc[:, column],
                      label=column)
    axis.legend()
fig.savefig(r"C:\Users\s1475174\Documents\Python_Projects\Thermal"
            r"Radiation_BREexperiments\plotting\onevariable_all"
            r"experiments/Flame_projection.png", dpi = 600)
plt.close(fig)