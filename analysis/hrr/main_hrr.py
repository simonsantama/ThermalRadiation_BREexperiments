"""
This codes takes the external HRR data from the unprocessed_data folder and saves it as a pickle in the processed_data
folder.

"""

import pandas as pd
import pickle

HRR = {}

# iterate over the four tests to be analysed
for test_name in ["Alpha2", "Beta1", "Beta2", "Gamma"]:
    
    # create an address to upload the file into a pandas data frame
    file_name = f"{test_name}_HRR.xlsx"
    file_address = f"C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/unprocessed_data/hrr_data/{file_name}"
    
    # data uploading must be done independently since these files have already been modified and are not consistent
    if test_name == "Alpha2":
        HRR[test_name] = pd.read_excel(file_address, sheet_name = "Sheet1", usecols = [0, 3], names = ["testing_time", "THRR"])
        HRR[test_name].loc[:, "testing_time"] = HRR[test_name].loc[:, "testing_time"] * 60
        
    elif test_name == "Beta1":
        HRR[test_name] = pd.read_excel(file_address, sheet_name = "HRR", usecols = [0, 8], names = ["testing_time", "THRR"])
        HRR[test_name].loc[:, "testing_time"] = HRR[test_name].loc[:, "testing_time"] * 60    

    elif test_name == "Beta2":
        HRR[test_name] = pd.read_excel(file_address, sheet_name = "Sheet1", usecols = [0, 1], names = ["testing_time", "THRR"])
        HRR[test_name].loc[:, "testing_time"] = HRR[test_name].loc[:, "testing_time"] * 60
        
    elif test_name == "Gamma":
        HRR[test_name] = pd.read_excel(file_address, sheet_name = "Sheet1", usecols = [0, 3], names = ["testing_time", "THRR"])
        HRR[test_name].loc[:, "testing_time"] = HRR[test_name].loc[:, "testing_time"] * 60

# save all the external HRR data as a pickle in processed data
file_address_save = f"C:/Users/s1475174/Documents/Python_Projects/BRE_Paper_2016/processed_data/HRR_total.pkl"
with open(file_address_save, 'wb') as handle:
    pickle.dump(HRR, handle)
