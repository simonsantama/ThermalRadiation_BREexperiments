"""
This script creates initial comparison plots to compare the data per
experiment
"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import pickle
import os
import numpy as np

# load data
address_processed_data = (r"C:\Users\s1475174\Documents\Python_Projects\T"
                          r"hermalRadiation_BREexperiments\processed_dat"
                          r"a\all_data_BREexperiments.pkl")

with open(address_processed_data, "rb") as handle:
    all_data = pickle.load(handle)

address_plots = (r"C:\Users\s1475174\Documents\Python_Projects\T"
                 r"hermalRadiation_BREexperiments\plotting\oneexperimen"
                 r"t_allvariables")

# dictionary wit video still times (text and vertical lines)
videostill_times = {
    "Alpha2": [2, 5.13, 14, 35, 58],
    "Beta1": [2.3, 8.5, 9.9, 20, 30],
    "Beta2": [1.3, 4.2, 10, 18, 26],
    "Gamma": [1.5, 5.4, 17, 39, 59]}
x_text = [5, 18, 30, 40, 55]

# data for Beta2 at time > 30 minutes was corrupted
all_data["Beta2"].loc[
    all_data["Beta2"].loc[:, "testing_time"] / 60 > 30, :] = np.nan

for exp, df in all_data.items():
    # create and format the figure
    fig, axes = plt.subplots(7, 1, figsize=(10,20), sharex=True)
    fig.suptitle(exp, fontsize=22)
    # first subplot is the video stills
    axes[0].axis("off")
    img = mpimg.imread(f"{exp}_stills.png")
    axes[0].imshow(img, aspect="auto", extent=[0, 60, 0, 100])

    for a, ax in enumerate(axes[1:]):
        ax.set_title(["HRR", "Velocities", "Heat Flux", "Temperature",
                      "Neutral Plane", "Flame Depth"][a], fontsize=20)
        ax.grid(True, linewidth=0.5, color="gainsboro", linestyle="--")
        ax.set_ylabel(["HRR [kW]", "Velocity [m]", "Heat Flux [kW/m2]",
                       "Temperature [C]", "Height [m]", "Depth [m]"][a],
                      fontsize=18)
        # plot vertical lines
        for t, time in enumerate(videostill_times[exp]):
            ax.plot([time, time], [0, 2000], linestyle="--", color="black",
                    linewidth=0.75)
            axes[0].text(s=f"{time} min", x=x_text[t] , y=90, color="white",
                         ha="center", va="center", fontweight="bold")


    axes[-1].set_xlabel("Time [min]", fontsize=18)
    axes[-1].set_xlim([0, 60])
    axes[-1].set_yticks(np.linspace(0, 60, 7))

    # plot the data
    for a, ax in enumerate(axes[1:]):
        if a == 0:  # HRR
            ax.set_ylim([0, 8])
            ax.set_yticks(np.linspace(0, 8, 5))
            ax.plot(df.loc[:, "testing_time"] / 60,
                    df.loc[:, "THRR"]/1000,
                    label="Total HRR")
            ax.plot(df.loc[:, "testing_time"] / 60,
                    df.loc[:, "hrr_internal_allmassin"]/1000,
                    label="Internal HRR")
            ax.legend(loc="upper right")

        elif a == 1:  # Velocities
            ax.set_ylim([0, 12])
            ax.set_yticks(np.linspace(0, 16, 5))
            for column in [f"V_{x}" for x in
                            np.linspace(100, 180, 5).astype("int")]:
                ax.plot(df.loc[:, "testing_time"] / 60,
                        - df.loc[:, column],
                        label=column.split("_")[1])
                ax.legend(loc="upper left", ncol=5, title="Height (mm)")

        elif a == 2:  # Thermal radiation
            if exp == "Beta1":
                continue
            ax.set_ylim([0, 50])
            ax.set_yticks(np.linspace(0, 50, 6))
            for column in [f"sIHF_{x}" for x in
                            np.linspace(0, 7, 8).astype("int")]:
                ax.plot(df.loc[:, "testing_time"] / 60,
                        df.loc[:, column] / 1000,
                        label=column)
                ax.legend(loc="upper left", ncol=7)

        elif a == 3:  # Temperatures
            ax.set_ylim([0, 1500])
            ax.set_yticks(np.linspace(0, 1500, 6))
            try:
                ax.plot(df.loc[:, "testing_time"] / 60,
                        df.loc[:, "TXX-180"],
                        label="Wall TC tree")
            except KeyError:
                print(f"TXX-180 not available for {exp}")
            ax.plot(df.loc[:, "testing_time"] / 60,
                    df.loc[:, "T22-180"],
                    label="Central TC tree")
            ax.plot(df.loc[:, "testing_time"] / 60,
                    df.loc[:, "TD180"],
                    label="Door TC tree")
            ax.legend(loc="lower right", title="T @ h=1.80 m")

        elif a == 4:  # Neutral plane
            ax.set_ylim([0, 1.5])
            ax.set_yticks(np.linspace(0, 1.5, 6))
            ax.plot(df.loc[:, "testing_time"] / 60,
                    df.loc[:, "Neutral_Plane_Smooth"])

        elif a == 5:
            ax.set_ylim([0, 2])
            ax.set_yticks(np.linspace(0, 2, 5))
            for c, column in enumerate([f"flame_depth_{h}_smooth" for h in [
                    "below", "topdoor", "above"]]):
                ax.plot(df.loc[:, "testing_time"] / 60,
                        df.loc[:, column],
                        label=("Depth at"
                               f" {['0.5 m below','','0.5 m above'][c]}"
                               " top of the door"))
            ax.legend(loc = "upper right", ncol=2)
            

    # save figure
    fig.subplots_adjust(top=0.95)
    fig.savefig(os.path.join(address_plots, exp))