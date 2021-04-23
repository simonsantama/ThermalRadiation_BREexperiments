"""
Plots the total Heat Release Rate for all experiments
"""

import pickle
import matplotlib.pyplot as plt
import numpy as np


test_name = ["Alpha1", "Alpha2", "Beta1", "Beta2", "Gamma"]

address_doorframe_fulldata = (r"C:/Users/s1475174/Documents/Python_Projects/T"
                              r"hermalRadiation_BREexperiments/processed_dat"
                              r"a/HRR_total.pkl")
with open(address_doorframe_fulldata, "rb") as handle:
    hrr_fulldata = pickle.load(handle)

# iterate over all the parameters I wish to plot
fontsize_legend = 6   
    
fig, ax = plt.subplots(5,1,figsize = (8,11), sharex = True)
fig.suptitle("Total HRR")
fig.subplots_adjust(top = 0.9)

ax[4].set_xlim([0,60])
ax[4].set_xticks(np.linspace(0,60,13))
ax[4].set_xlabel("Time [min]")

for i, axis in enumerate(ax):
    if test_name[i] == "Alpha1":
        continue
    # format the subplots
    axis.set_ylabel("HRR [MW]")
    axis.set_ylim([0, 8])
    axis.grid(True, linestyle = "--", color = "gainsboro")
    axis.set_title(test_name[i])

    # extract data
    df = hrr_fulldata[test_name[i]]

    # plot
    mask = (df.loc[:, "testing_time"] > 0) & (df.loc[
        :,"testing_time"]/60 < 60)
    axis.plot(df.loc[:, "testing_time"]/60,
              df.loc[:, "THRR"]/1000)

fig.savefig(r"C:\Users\s1475174\Documents\Python_Projects\Thermal"
            r"Radiation_BREexperiments\plotting\onevariable_all"
            r"experiments/HRR_total.png", dpi = 600)
plt.close(fig)

    
    