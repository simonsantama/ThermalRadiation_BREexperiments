"""
This script uploads the dictionary with the raw flame dimensions data, smoothes the data using
Savitsky-Golay and then saves that into the processed data folder

"""
# import libraries
import pickle
from scipy.signal import savgol_filter

# import the unsmoothed flame dimensions data
file_address_save = "Flame_Dimensions_unsmoothed.pkl"
with open(file_address_save, 'rb') as handle:
    Flame_Dimensions = pickle.load(handle)
    
# define the smoothing parameters
window_length = 61
polyorder = 2

# smooth the data of each column
for experiment in Flame_Dimensions:
    for column in Flame_Dimensions[experiment]:
        if "time" in column:
            continue
        else:
            smooth_column_name = f"{column}_smooth"
            Flame_Dimensions[experiment].loc[:, smooth_column_name] = savgol_filter(Flame_Dimensions[experiment].loc[:, column],
                            window_length, polyorder)

# save into the processed data folder
file_address_save = f"C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/Flame_Dimensions.pkl"
with open(file_address_save, 'wb') as handle:
    pickle.dump(Flame_Dimensions, handle)
