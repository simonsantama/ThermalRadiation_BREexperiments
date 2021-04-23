"""
This script plots the TSC data for all experiments and saves it in the
plotting folder
"""

import pickle
import matplotlib.pyplot as plt
import numpy as np


# load TSC data
file_address_load = (r"C:/Users/s1475174/Documents/Python_Projects/T"
                     r"hermalRadiation_BREexperiments/processed_data/TSC.pkl")
with open(file_address_load, 'rb') as handle:
    all_data = pickle.load(handle)



# Plotting 
test_name = ["Alpha2", "Beta2", "Gamma"]
fontsize_legend = 6   
heights = [0.6, 1.1, 1.6, 2.1]
distances = ["2m", "4m"]
labels = [None]
for d in distances:
    for h in heights:
        labels.append(f"{d}-{h}")

fig, ax = plt.subplots(3,1,figsize = (8,11), sharex = True)
fig.suptitle("Total HRR")
fig.subplots_adjust(top = 0.9)

ax[2].set_xlim([0,60])
ax[2].set_xticks(np.linspace(0,60,13))
ax[2].set_xlabel("Time [min]")

for i, axis in enumerate(ax):

    # format the subplots
    axis.set_ylabel("HRR [MW]")
    axis.set_ylim([0, 40])
    axis.grid(True, linestyle="--", color="gainsboro")
    axis.set_title(test_name[i])

    # extract data
    df = all_data[test_name[i]]

    # plot
    mask = (df.loc[:, "testing_time"] > 0) & (df.loc[
        :,"testing_time"]/60 < 60)
    for c, column in enumerate(df.columns):
        if "testing" in column:
            continue
        axis.plot(df.loc[:, "testing_time"]/60,
                  df.loc[:, column]/1000,
                  label=labels[c])
    axis.legend(ncol=2)

fig.savefig(r"C:\Users\s1475174\Documents\Python_Projects\Thermal"
            r"Radiation_BREexperiments\plotting\onevariable_all"
            r"experiments/ThermalRadiation.png", dpi = 600)
plt.close(fig)

    
    